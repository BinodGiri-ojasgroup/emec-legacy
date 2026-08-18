from django.contrib import admin

from apps.testimonials.models import Client, Testimonial


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("name", "is_featured", "display_order")
    list_editable = ("is_featured", "display_order")


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ("author_name", "client", "is_featured", "display_order")
    list_editable = ("is_featured", "display_order")
