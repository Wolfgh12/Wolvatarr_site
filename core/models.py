from django.db import models

class ProjectTransmission(models.Model):
    SERVICE_CHOICES = [
        ('web', 'Custom Web & System Development (Django/Python)'),
        ('video', 'Cinematic Video & 3D Motion Commercials'),
        ('brand', 'Brand Identity & Graphic Design Suite'),
        ('full_pack', 'The Full Arsenal (Web + Video + Branding)'),
    ]

    TIMELINE_CHOICES = [
        ('rush', 'Rush Priority (2 - 3 Weeks)'),
        ('standard', 'Standard Sprint (4 - 6 Weeks)'),
        ('flexible', 'Flexible / Planning Phase'),
    ]

    name = models.CharField(max_length=150, help_text="Client full name")
    email = models.EmailField(help_text="Client contact email")
    service = models.CharField(max_length=50, choices=SERVICE_CHOICES, help_text="Requested capability")
    timeline = models.CharField(max_length=50, choices=TIMELINE_CHOICES, default='standard', help_text="Target launch timeline")
    message = models.TextField(help_text="Detailed project brief and vision")
    is_reviewed = models.BooleanField(default=False, help_text="Mark whether the brief has been reviewed by the lead architect")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Project Transmission'
        verbose_name_plural = 'Project Transmissions'

    def __str__(self):
        return f"{self.name} | {self.get_service_display()} ({self.created_at.strftime('%Y-%m-%d')})"


class ActiveInterceptConfig(models.Model):
    """
    Singleton control switch for Wolvatarr Active Intercept™ defenses.
    Allows toggling perimeter protection, keyboard intercepts, debugger loops, and honeypots from Django Admin.
    """
    is_armed = models.BooleanField(
        default=True,
        help_text="Master Switch: Arm or disarm all Active Intercept client defenses."
    )
    block_context_menu = models.BooleanField(
        default=True,
        help_text="Disable mouse right-click context menu and inspect elements."
    )
    block_devtools_keys = models.BooleanField(
        default=True,
        help_text="Block inspection shortcuts (F12, Ctrl+Shift+I/J/C, Ctrl+U, Cmd+Opt+I)."
    )
    debugger_poison_loop = models.BooleanField(
        default=True,
        help_text="Poison Trap: Execute recursive debugger lock if DevTools opens or detaches."
    )
    honeypot_traps = models.BooleanField(
        default=True,
        help_text="Honeypot Trap: Silently transmit intrusion payloads and IP telemetry to the admin vault."
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Active Intercept Configuration'
        verbose_name_plural = 'Active Intercept Configuration'

    def save(self, *args, **kwargs):
        # Guarantee singleton pattern (always ID 1)
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get_config(cls):
        config, _ = cls.objects.get_or_create(
            pk=1,
            defaults={
                'is_armed': True,
                'block_context_menu': True,
                'block_devtools_keys': True,
                'debugger_poison_loop': True,
                'honeypot_traps': True,
            }
        )
        return config

    def __str__(self):
        state = "ARMED" if self.is_armed else "DISARMED"
        return f"Active Intercept Sentinel :: [{state}]"


class SecurityIncidentLog(models.Model):
    """
    Honeypot incident log recording IP, user agent, and intrusion attempt vectors.
    """
    INCIDENT_TYPES = [
        ('KEY_INTERCEPT', 'Shortcut Key Intercept (F12 / Inspect / View-Source)'),
        ('CONTEXT_MENU', 'Context Menu / Right-Click Inspect'),
        ('DEVTOOLS_DETECTED', 'DevTools Perimeter Breach Detected'),
        ('DEBUGGER_TRAP', 'Poison Loop Triggered'),
        ('HONEYPOT_PROBE', 'Decoy Endpoint Probed'),
    ]

    ip_address = models.GenericIPAddressField(null=True, blank=True, help_text="Intruder IP address")
    user_agent = models.TextField(blank=True, help_text="Browser client fingerprint")
    incident_type = models.CharField(max_length=40, choices=INCIDENT_TYPES, default='KEY_INTERCEPT')
    details = models.TextField(blank=True, help_text="Telemetry payload or specific key combo")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Security Incident Log'
        verbose_name_plural = 'Security Incident Logs'

    def __str__(self):
        return f"[{self.incident_type}] {self.ip_address} @ {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"


# --- DYNAMIC PORTFOLIO ARCHITECTURE ---

class PortfolioProject(models.Model):
    CATEGORY_CHOICES = [
        ('web', 'Web & Systems'),
        ('motion', 'Video & 3D Motion'),
        ('brand', 'Brand & Identity'),
    ]

    title = models.CharField(max_length=200, help_text="e.g. Encrypted Legacy Registry & Custody Vault")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='web')
    sector = models.CharField(max_length=150, help_text="e.g. SECTOR // FINTECH & IDENTITY INFRASTRUCTURE")
    badge_code = models.CharField(max_length=50, blank=True, help_text="e.g. [SYS.01 // VAULT] or 4K STUDIO")
    result_metric = models.CharField(max_length=100, help_text="e.g. Zero-Knowledge Security or 1.2M+ Reach Footprint")
    description = models.TextField(help_text="Capability summary and business outcome")
    tech_tags = models.CharField(max_length=255, help_text="Comma-separated tags (e.g. Python 3.12, Django ASGI, PostgreSQL)")
    cover_image = models.ImageField(upload_to='portfolio/covers/', help_text="Main high-res card display image")
    external_link = models.URLField(blank=True, null=True, help_text="Optional live deployment URL (leave blank to route to /contact/)")
    link_text = models.CharField(max_length=60, default="Commission Platform &rarr;")
    display_order = models.PositiveIntegerField(default=0, help_text="Order on page (0 shows first)")
    is_active = models.BooleanField(default=True, help_text="Toggle visibility on the public portfolio")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['display_order', '-created_at']
        verbose_name = 'Portfolio Project'
        verbose_name_plural = 'Portfolio Projects'

    def __str__(self):
        return f"[{self.get_category_display()}] {self.title}"

    def get_tag_list(self):
        """Splits comma-separated tags for template chips"""
        return [tag.strip() for tag in self.tech_tags.split(',') if tag.strip()]


class ProjectScreenshot(models.Model):
    project = models.ForeignKey(PortfolioProject, on_delete=models.CASCADE, related_name='screenshots')
    image = models.ImageField(upload_to='portfolio/gallery/')
    caption = models.CharField(max_length=150, blank=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['display_order', 'id']
        verbose_name = 'Project Screenshot'
        verbose_name_plural = 'Project Screenshots'

    def __str__(self):
        return f"{self.project.title} Screenshot #{self.display_order}"


# --- PERSISTENT PILOT PROFILE & REAL DATABASE LEADERBOARD ---

class ArcadePilot(models.Model):
    callsign = models.CharField(max_length=50, unique=True, help_text="Pilot rank and name (e.g. AGENT NANA)")
    high_score = models.PositiveIntegerField(default=0)
    highest_wave = models.PositiveIntegerField(default=1)
    saved_wave = models.PositiveIntegerField(default=1)
    saved_score = models.PositiveIntegerField(default=0)
    weapon_level = models.PositiveIntegerField(default=1)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-high_score', '-highest_wave']
        verbose_name = 'Arcade Pilot'
        verbose_name_plural = 'Arcade Pilots'

    def __str__(self):
        return f"{self.callsign} | High Score: {self.high_score} (Wave {self.highest_wave})"