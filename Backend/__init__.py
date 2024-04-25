from .celery import app as celery_app
import matplotlib
matplotlib.use('Agg')

__all__ = ("celery_app",)