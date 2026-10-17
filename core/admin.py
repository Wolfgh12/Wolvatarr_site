from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .models import (
    ProjectTransmission,
    ActiveInterceptConfig,
    SecurityIncidentLog,
    PortfolioProject,
    ProjectScreenshot,
    ArcadePilot
)


@admin.register(ArcadePilot)
class ArcadePilotAdmin(admin.ModelAdmin):
    list_display = ('callsign', 'high_score', 'highest_wave', 'saved_wave', 'weapon_level', 'updated_at')
    search_fields = ('callsign',)
    ordering = ('-high_score',)

# Wolvatarr Command Dashboard Branding
admin.site.site_header = "Wolvatarr Command Console"
admin.site.site_title = "Wolvatarr Admin Portal"
admin.site.index_title = "Digital Architecture & Inbound Transmissions"


class ProjectScreenshotInline(admin.TabularInline):
    model = ProjectScreenshot
    extra = 3
    fields = ('image', 'caption', 'display_order', 'preview_image')
    readonly_fields = ('preview_image',)

    def preview_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height: 50px; border-radius: 6px; border: 1px solid #38bdf8;" />', obj.image.url)
        return "-"
    preview_image.short_description = "Preview"


@admin.register(PortfolioProject)
class PortfolioProjectAdmin(admin.ModelAdmin):
    list_display = ('cover_preview', 'title', 'category', 'display_order', 'is_active', 'created_at')
    list_filter = ('category', 'is_active', 'created_at')
    list_editable = ('display_order', 'is_active')
    search_fields = ('title', 'sector', 'description', 'tech_tags')
    inlines = [ProjectScreenshotInline]

    fieldsets = (
        ("Core Identity", {
            "fields": ("title", "category", "sector", "badge_code", "result_metric")
        }),
        ("Media & Visuals", {
            "fields": ("cover_image", "description", "tech_tags")
        }),
        ("Deployment Link & Display", {
            "fields": ("external_link", "link_text", "display_order", "is_active")
        }),
    )

    def cover_preview(self, obj):
        if obj.cover_image:
            return format_html('<img src="{}" style="height: 40px; width: 65px; object-fit: cover; border-radius: 6px; border: 1px solid #00d4ff;" />', obj.cover_image.url)
        return "No Cover"
    cover_preview.short_description = "Cover"


@admin.register(ProjectTransmission)
class ProjectTransmissionAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'service', 'timeline', 'is_reviewed', 'created_at')
    list_filter = ('is_reviewed', 'service', 'timeline', 'created_at')
    search_fields = ('name', 'email', 'message')
    list_editable = ('is_reviewed',)
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'

    actions = ['mark_as_reviewed']

    @admin.action(description="Mark selected transmissions as reviewed")
    def mark_as_reviewed(self, request, queryset):
        rows_updated = queryset.update(is_reviewed=True)
        self.message_user(request, f"{rows_updated} transmission(s) successfully marked as reviewed.")


@admin.register(ActiveInterceptConfig)
class ActiveInterceptConfigAdmin(admin.ModelAdmin):
    """
    Direct control switch for Active Intercept.
    Toggles can be switched on/off right in the list view table with one click.
    """
    list_display = (
        'status_indicator',
        'is_armed',
        'block_context_menu',
        'block_devtools_keys',
        'debugger_poison_loop',
        'honeypot_traps',
        'updated_at'
    )
    list_editable = (
        'is_armed',
        'block_context_menu',
        'block_devtools_keys',
        'debugger_poison_loop',
        'honeypot_traps'
    )
    actions = ['arm_all_defenses', 'disarm_all_defenses']

    def status_indicator(self, obj):
        if obj.is_armed:
            return mark_safe(
                '<span style="background: rgba(0, 255, 204, 0.15); color: #00ffcc; '
                'border: 1px solid #00ffcc; padding: 4px 10px; border-radius: 20px; '
                'font-weight: 800; font-family: monospace;">● ARMED</span>'
            )
        return mark_safe(
            '<span style="background: rgba(239, 68, 68, 0.15); color: #ef4444; '
            'border: 1px solid #ef4444; padding: 4px 10px; border-radius: 20px; '
            'font-weight: 800; font-family: monospace;">○ DISARMED</span>'
        )
    status_indicator.short_description = "Status"

    def has_add_permission(self, request):
        if ActiveInterceptConfig.objects.exists():
            return False
        return super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        return False

    @admin.action(description="⚡ ARM Active Intercept (Full Lockdown)")
    def arm_all_defenses(self, request, queryset):
        queryset.update(
            is_armed=True,
            block_context_menu=True,
            block_devtools_keys=True,
            debugger_poison_loop=True,
            honeypot_traps=True
        )
        self.message_user(request, "Active Intercept Sentinel: ALL perimeter layers ARMED.")

    @admin.action(description="🛑 DISARM Active Intercept (Allow Inspection)")
    def disarm_all_defenses(self, request, queryset):
        queryset.update(is_armed=False)
        self.message_user(request, "Active Intercept Sentinel: DISARMED. Browser inspection permitted.")


@admin.register(SecurityIncidentLog)
class SecurityIncidentLogAdmin(admin.ModelAdmin):
    """
    Live honeypot log view of all intrusion and inspection attempts.
    """
    list_display = ('incident_badge', 'ip_address', 'created_at')
    list_filter = ('incident_type', 'created_at')
    search_fields = ('ip_address', 'user_agent', 'details')
    readonly_fields = ('ip_address', 'user_agent', 'incident_type', 'details', 'created_at')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'

    def incident_badge(self, obj):
        colors = {
            'KEY_INTERCEPT': '#eab308',
            'CONTEXT_MENU': '#38bdf8',
            'DEVTOOLS_DETECTED': '#f97316',
            'DEBUGGER_TRAP': '#ef4444',
            'HONEYPOT_PROBE': '#a855f7',
        }
        color = colors.get(obj.incident_type, '#ef4444')
        return format_html(
            '<span style="color: {}; font-weight: 800; font-family: monospace;">⚠ {}</span>',
            color,
            obj.get_incident_type_display(),
        )
    incident_badge.short_description = "Incident Type"

    def has_add_permission(self, request):
        return False