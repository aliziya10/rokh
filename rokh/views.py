import math

from django.core.paginator import Paginator
from django.db.models import OuterRef, Subquery
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .serializers import *
from home.models import *
from Posts.models import *
from accounts.models import *
from rest_framework.generics import get_object_or_404

@permission_classes([AllowAny])
@api_view(["POST","GET"])
def contactus(request):
    try:
        ContactUs.objects.get_or_create(
            name=request.data["name"],
            email=request.data["email"],
            mobile=request.data["mobile"],
            comment=request.data["comment"],
        )
        return JsonResponse({"message": "comment saved"})


    except:
        return JsonResponse({"error":"fill all fields(name,mobile,email,comment)"})


@api_view(["GET"])
@permission_classes([AllowAny])
def home(request):
    res={}
    base_url = "https://storage.iran.liara.space/hanousa/static/"

    url = "https://server.rokhdental.ir/images/"

    slides = Slides.objects.filter(status=1)

    res["slides"]=slides.values()

    posts = Post.objects.filter(status=1)

    res["posts"]=posts.annotate(
        img=Subquery(
                    ImagePost.objects.filter(post_id=OuterRef('id')).values('image')[:1]
                )
    ).values('id',"title","sub_title",'img',"persian_date",'author__username').order_by("-id")[:3]



    ex=Expertise.objects.values('id','title')[:4]

    res['expertise']=ex

    info=RokhInfo.objects.values()
    res['information']:info
    # res["teammates"]=teammates.values("id","image_url","label","link")


    return Response(res)

@api_view(["GET"])
@permission_classes([AllowAny])
def layout(request):
    menus = list(Menu.objects.values())
    settings=RokhInfo.objects.values()
    return Response({"menus": menus,"settings":settings})

@api_view(["GET"])
@permission_classes([AllowAny])
def special_post(request,adressurl):
    base_url = "https://server.hanousa.ir/images/"
    # poli="id","title","sub_title","image_url","dateOfPublish","author"

    try:
        # tag_list = Post.objects.filter(tags__blogs=adressurl).values("tags__title")
        #
        # posts = Post.objects.values("id","title","text","sub_title","image_url","persian_date","author__username",'tags__title').get(id=adressurl)
        # d = posts
        # d['tags'] = tag_list
        # # image_url=Concat(Value(base_url), F('image'), output_field=CharField()),
        tag_list = Post.objects.filter(tags__blogs=adressurl).values("tags__title")


        posts = Post.objects.values("id","title","text","sub_title","image_url","persian_date","author__username").get(id=adressurl)
        d = posts
        d['tags'] = tag_list
        # image_url=Concat(Value(base_url), F('image'), output_field=CharField()),

        posts = Post.objects.get(id=adressurl)
        d = get_object_or_404(Post, id=adressurl)
        se = PostSerializers(d)


        return Response(se.data, status=status.HTTP_200_OK)

    except (ValueError,Post.DoesNotExist):
        return Response({},status=status.HTTP_404_NOT_FOUND)



@api_view(["POST","GET"])
@permission_classes([AllowAny])
def post_list(request,page):
    try:
        base_url = "https://server.hanousa.ir/images/"
        posts = Post.objects.all()
        paginator = Paginator(posts, 8)
        page_obj = paginator.get_page(page)
        num_pages = paginator.num_pages
        return Response({"posts":page_obj.object_list.values("id","title","image_url"),"page_count":num_pages})
    except:
        return Response({"message":"not found."},status=status.HTTP_404_NOT_FOUND)
