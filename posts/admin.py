from django.contrib import admin

from posts.models import Posts, Images, Categories, Comments


@admin.register(Posts)
class PostAdmin(admin.ModelAdmin):
    model = Posts
    list_display = (
        "title", "description", "date_publication", "user"
    )
    list_filter = ("title", "date_publication", "user")
    search_fields = ("title", "user")


@admin.register(Images)
class ImageAdmin(admin.ModelAdmin):
    model = Images
    list_display = ("image", "post")
    list_filter = ("post",)
    search_fields = ("post",)


@admin.register(Categories)
class CategoryAdmin(admin.ModelAdmin):
    model = Categories
    # list_display = ("title", "post")
    search_fields = ("title",)

@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    model = Comments
    list_display = ("author", "text", "likes", "dislikes", "created_at", "parent_comment")
    search_fields = ("author", "text")
    list_filter = ("created_at",)
    list_per_page = 50