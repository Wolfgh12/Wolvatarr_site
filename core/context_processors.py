from .models import ActiveInterceptConfig

def security_context(request):
    """
    Exposes Wolvatarr Active Intercept™ configuration variables
    globally across all Django templates.
    """
    try:
        config = ActiveInterceptConfig.get_config()
    except Exception:
        # Safe fallback during migrations or database initialization
        config = None

    return {
        'security_config': config
    }