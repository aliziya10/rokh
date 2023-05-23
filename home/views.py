from PIL.PngImagePlugin import _idat
from django.contrib.auth.decorators import user_passes_test
from django.db.models.functions import Concat
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, FileResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from rest_framework import renderers, status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated, BasePermission
from rest_framework.views import APIView
from accounts.models import User
from Posts.models import Post,ImagePost
from home.models import *
from django.db.models import F, OuterRef, Subquery, Q
from django.db.models.functions import Concat
from django.db.models import Value, F, CharField
from accounts.models import *
from accounts.serializers import *

base_url='https://server.rokhdental.ir'
@api_view(["GET"])
@permission_classes([IsAuthenticated, ])
@user_passes_test(lambda u: u.is_staff)
def page_home(request):
    doctor = User.objects.filter(is_doctor=True).count()
    admin = User.objects.filter(is_staff=True).count()
    post_count = Post.objects.count()
    request_per_day = 500
    ticket_count = ContactUs.objects.filter(is_answer=False).count()


    return Response({
        "doctor": doctor,
        "admin":admin,
        "post_count": post_count,
        "request_per_day": request_per_day,
        "ticket_count": ticket_count,
    })


@api_view(["GET", "POST", "DELETE","PUT"])
@permission_classes([IsAuthenticated])
@user_passes_test(lambda u: u.is_superuser)
def admin_list(request,pk=None):

    if request.method == "GET":
        if pk == None:
            admins = User.objects.values("id", "username", "phone", "is_active",'is_doctor','is_superuser','is_staff')
            return Response(admins)
        else:
            user=User.objects.values().get(id=pk)
            return Response(user)
    elif request.method == "POST":
        if "username" not in request.data or "password" not in request.data or "password2" not in request.data or "is_doctor" not in request.data or "is_staff" not in request.data:
            return Response({"message": "fill all fields"})
        name = request.data["username"]
        password = request.data["password"]
        password2 = request.data["password2"]
        is_doctor= request.data["is_doctor"]
        is_staff= request.data["is_staff"]


        if password != password2:
            return Response({"message": "passwords not match"})

        try:
            user = User.objects.create(
                username=name,
                is_staff=is_staff,
                is_doctor=is_doctor
            )
            user.set_password(password)
            user.save()
            return Response({"message": "user created"})

        except:
            return Response({"message":"this user is already staff"})

    elif request.method == "DELETE":
        try:
            user = User.objects.get(id=pk)
            if user.is_superuser == True:
                return Response({"message": "you can not change a superuser"})
            if user.is_active == False:
                return Response({"message": "this user is already not active"})
            else:
                user.is_active = False
                user.save()
                return Response({"message": "this user now is not active"})
        except:
            return Response({"message": "id not exist"})

    elif request.method=="PUT":
        try:
            user=User.objects.get(id=pk)
            if "is_doctor" in request.data:
                user.is_doctor=request.data["is_doctor"]
            if "is_superuser" in request.data:
                user.is_superuser=request.data["is_superuser"]
            if 'is_staff' in request.data:
                user.is_staff=request.data["is_staff"]
            if 'is_active' in request.data:
                user.is_active = request.data["is_active"]
            user.save()
            return Response({"message": "user changed"})
        except:
            return Response({"message":"user not found"})


@api_view(["GET", "PUT", "DELETE", "POST"])
@permission_classes([IsAuthenticated, ])
@user_passes_test(lambda u: u.is_staff)
def slide_list(request, pk=None):
    if request.method == "GET":
        if pk is None:
            slides = Slides.objects.all().values()
            return Response(slides)
        else:
            try:
                slide = Slides.objects.values().get(id=pk)
                return Response(slide)
            except:
                return Response({"message": "id not found"})
    elif request.method == "DELETE":
        try:
            slide = Slides.objects.get(id=pk).delete()
            return Response({"message": "slide deleted"})
        except:
            return Response({"message": "id not found"})
    elif request.method == "POST":
        if "title" not in request.POST or "text" not in request.POST or "image" not in request.FILES or "status" not in request.POST:
            return Response({"message":"enter all fields"})

        try:
            slide = Slides.objects.create(
                title=request.POST["title"],
                text=request.POST["text"],
                image=request.FILES["image"],
                status=request.POST["status"]
            )
            slide.save()
            slide.image_url=slide.image.url
            slide.save()
            return Response({"message": "slide created"})

        except:
            return Response({'message':"slide not created (for som reason)"})


    elif request.method == "PUT":
        try:
            slide = Slides.objects.get(id=pk)
            if "title" in request.POST:
                slide.title = request.POST["title"]
            if "text" in request.POST:
                slide.text = request.POST["text"]
            if "image" in request.FILES:
                slide.image = request.FILES["image"]
                slide.save()
                slide.image_url=slide.image.url
            if "status" in request.POST:
                slide.status = request.POST["status"]

            slide.save()
            return Response({"message": "slide changed"})
        except:
            return Response({"message": "id not found"})



@api_view(["GET", "DELETE", "PUT", "POST"])
@permission_classes([IsAuthenticated, ])
@user_passes_test(lambda u: u.is_staff)
def menu_list(request, pk=None):
    if request.method == "GET":
        if pk == None:
            menus = Menu.objects.all().annotate(
                parent_name=Subquery(
                    Menu.objects.filter(id=OuterRef('parent_id')).values('title')[:1]
                )
            ).values()
            return Response(menus)
        else:
            try:
                menu = Menu.objects.values().get(id=pk)
                return Response(menu)
            except:
                return Response({"message": "id not found"})
    elif request.method == "DELETE":
        try:
            menu = Menu.objects.get(id=pk).delete()
            return Response({"message": "menu deleted"})
        except:
            return Response({"message": "id not found"})

    elif request.method == "POST":
        if "title" not in request.data or "link" not in request.data or "parent_id" not in request.data or "type" not in request.data:
            return Response({"message": "enter all fields"})
        menu = Menu.objects.create(
            title=request.data["title"],
            link=request.data["link"],
            parent_id=request.data["parent_id"],
            type=request.data["type"]
        ).save()
        return Response({"message": "menu created"})

    elif request.method == "PUT":
        try:
            menu = Menu.objects.get(id=pk)
            if "title" in request.data:
                menu.title = request.data["title"]
            if "link" in request.data:
                menu.link = request.data["link"]
            if "parent_id" in request.data:
                menu.parent_id = request.data["parent_id"]
            if "type" in request.data:
                menu.type = request.data["type"]

            menu.save()
            return Response({"message": "menu changed"})
        except:
            return Response({"message": "id not found"})


@api_view(["GET", "PUT", "DELETE","POST"])
@permission_classes([IsAuthenticated, ])
@user_passes_test(lambda u: u.is_active)
def tickets_list(request, pk=None):
    if request.method == "GET":
        if pk == None:
            tickets = ContactUs.objects.all()
            tickets=tickets.annotate(
                answer=Subquery(
                    TicketAnswer.objects.filter(ticket_id=OuterRef('id')).values('answer')[:1]
                )
            ).values()
            return Response(tickets.order_by("is_answer","-id"))
        else:
            try:
                tickets = ContactUs.objects
                tickets = tickets.annotate(
                    answer=Subquery(
                        TicketAnswer.objects.filter(ticket_id=OuterRef('id')).values('answer')[:1]
                    )
                ).values().get(id=pk)
                return Response(tickets)
            except:
                return Response({"message": "id not found"})

    elif request.method == "DELETE":
        try:
            ContactUs.objects.get(id=pk).delete()
            return Response({"message": "ticket deleted"})
        except:
            return Response({"message": "id not found"})

    # elif request.method == "PUT":
    #     try:
    #         contact = ContactUs.objects.get(id=pk)
    #         if "answer" in request.data:
    #
    #
    #
    #             return Response({"message": "comment changed"})
    #         else:
    #             return Response({"message": "enter is_suggest field"})
    #     except:
    #         return Response({"message": "id not found"})


    elif request.method == "POST":
        if "answer" not in request.data or "id" not in request.data or pk==None:
            return Response({"message":"fill all fields"})

        try:
            answer=TicketAnswer.objects.create(
                answer=request.data["answer"],
                name=User.objects.get(id=request.data["id"]).username,
                ticket_id=ContactUs.objects.get(id=pk)
            ).save()
            c=ContactUs.objects.get(id=pk)
            c.is_answer=True
            c.save()
            return Response({"message":"answer created"})
        except:
            return Response({"message":"User or ticket id not found"})





@api_view(['POST', 'PUT', 'DELETE',"GET"])
@permission_classes([IsAuthenticated])
@user_passes_test(lambda u: u.is_staff)
def posts_list(request, pk=None):
    if request.method == "GET":
        if pk is None:
            posts = Post.objects.all()
            posts=posts.annotate(
                author_name=Concat('author__username',Value(''))
            ).values()
            return Response(posts)
        else:
            try:
                post = Post.objects.annotate(
                    author_name=Concat('author__username',Value(''))
                ).values().get(id=pk)
                return Response(post)
            except:
                return Response({"message": "id not found"})
    elif request.method == "DELETE":
        try:
            post = Post.objects.get(id=pk).delete()
            return Response({"message": "post deleted"})
        except:
            return Response({"message": "id not found"})

    elif request.method == "POST":
        if "title" not in request.POST or "sub_title" not in request.POST or "text" not in request.POST or "status" not in request.POST or "id" not in request.POST:
            return Response({"message": "enter all fields"})

        try:
            post = Post.objects.create(
                title=request.POST["title"],
                sub_title=request.POST["sub_title"],
                text=request.POST["text"],
                status=request.POST["status"],
                author=User.objects.get(id=request.POST["id"])
            )
            if "image" in request.FILES:
                post.image=request.FILES["image"]
                post.save()
                post.image_url = post.image.url

            post.save()


            return Response({"message": "post created"})

        except:
            return Response({'message': "post not created (for some reason)"})


    elif request.method == "PUT":
        try:
            post = Post.objects.get(id=pk)
            if "title" in request.POST:
                post.title = request.POST["title"]
            if "sub_title" in request.POST:
                post.sub_title=request.POST["sub_title"]
            if "text" in request.POST:
                post.text = request.POST["text"]
            if "image" in request.FILES:
                post.image = request.FILES["image"]
                post.save()
                post.image_url=post.image.url
            if "status" in request.POST:
                post.status = request.POST["status"]

            post.save()
            return Response({"message": "post changed"})
        except:
            return Response({"message": "id not found"})



@api_view(["GET", "PUT", "DELETE", "POST"])
@permission_classes([IsAuthenticated, ])
@user_passes_test(lambda u: u.is_staff)
def teammate_list(request, pk=None):
    if request.method == "GET":
        if pk is None:
            teams = Teammate.objects.all().values()
            return Response(teams)
        else:
            try:
                team = Teammate.objects.values().get(id=pk)
                return Response(team)
            except:
                return Response({"message": "id not found"})

    elif request.method == "DELETE":
        try:
            team = Teammate.objects.get(id=pk).delete()
            return Response({"message": "teammate deleted"})
        except:
            return Response({"message": "id not found"})
    elif request.method == "POST":
        if "label" not in request.POST or "image" not in request.FILES or "link" not in request.POST:
            return Response({"message":"enter all fields"})

        try:
            team = Teammate.objects.create(
                label=request.POST["label"],
                link=request.POST["link"],
                image=request.FILES["image"],
            ).save()

            team.image_url = team.image.url
            team.save()
            return Response({"message": "teammate created"})

        except:
            return Response({'message':"teammate not created (for some reason)"})


    elif request.method == "PUT":
        try:
            team = Teammate.objects.get(id=pk)
            if "label" in request.POST:
                team.label = request.POST["label"]
            if "link" in request.POST:
                team.link = request.POST["link"]
            if "image" in request.FILES:
                team.save()
                team.image_url = team.image.url
                team.image = request.FILES["image"]

            team.save()
            return Response({"message": "teammate changed"})
        except:
            return Response({"message": "id not found"})








@api_view(["GET", "PUT"])
@permission_classes([IsAuthenticated, ])
@user_passes_test(lambda u: u.is_superuser)
def mainsettings(request):
    if request.method == "GET":
        try:
            info = RokhInfo.objects.values().first()
            return Response(info)
        except:
            return Response({"massage": "enter information"})

    elif request.method == "PUT":
        try:
            info = RokhInfo.objects.first()
            if "name" in request.POST:
                info.name = request.POST["name"]
            if "number" in request.POST:
                info.number = request.POST["number"]
            if "address" in request.POST:
                info.address = request.POST["address"]
            if "email" in request.POST:
                info.email=request.POST["email"]
            if "description" in request.POST:
                info.description = request.POST["description"]
            if "image" in request.FILES:
                info.image=request.FILES["image"]
                info.save()
                info.image_url=info.image.url
            info.save()
            return Response({"message": "information updated"})
        except:
            return Response({"massage": "enter information"})

# @api_view(["GET"])
# def doctor_profile(request, id):
#     if request.method == "GET":
#         try:
#             doctr = Profile.objects.values("name", 'bio', "pezeshki_code", "profile_image", 'working_hour', "expertise",
#                                            "birth_year").get(id=id)
#             return Response(doctr, status=200)
#         except:
#             return Response({"massage": "doctr is not exsit"})


class DrProfileView(APIView):
    def get(self, request, id):
        try:
            profile = Profile.objects.get(id=id)
            serializer = ProfileSerializer(profile)
            return Response(serializer.data)
        except Profile.DoesNotExist:
            return Response({'error': 'DrProfile not found'}, status=404)






@api_view(["GET", "PUT", "DELETE", "POST"])
@permission_classes([IsAuthenticated, ])
@user_passes_test(lambda u: u.is_active)
def expertise_list(request, pk=None):
    if request.method == "GET":
        if pk is None:
            expertise = Expertise.objects.all().values()
            return Response(expertise)
        else:
            # try:
                a=get_object_or_404(Expertise,id=pk)
                ex=ExpertiseSelializer(a)
                dd=ex.data
                dd['image']=base_url + ex.data.get('image')

                return Response(dd)
            # except:
                # return Response({"message": "id not found"})
    elif request.method == "DELETE":
        try:
            expertise = Expertise.objects.get(id=pk).delete()
            return Response({"message": "expertise deleted"})
        except:
            return Response({"message": "id not found"})
    elif request.method == "POST":
        if "title" not in request.POST or "image" not in request.FILES:
            return Response({"message":"enter all fields"})

        try:
            expertise = Expertise.objects.create(
                title=request.POST["title"],
                image=request.FILES["image"],
            )
            expertise.save()
            expertise.image_url=expertise.image.url
            if "text" in request.POST:
                expertise.text = request.POST['text']

            expertise.save()

            return Response({"message": "expertise created"})

        except:
            return Response({'message':"expertise not created (for som reason)"})


    elif request.method == "PUT":
        try:
            expertise = Expertise.objects.get(id=pk)
            if "title" in request.POST:
                expertise.title = request.POST["title"]
            if "text" in request.POST:
                expertise.text = request.POST["text"]
            if "image" in request.FILES:
                expertise.image = request.FILES["image"]
                expertise.save()
                expertise.image_url=expertise.image.url
            expertise.save()
            return Response({"message": "expertise changed"})
        except:
            return Response({"message": "id not found"})


class Exampleclass(viewsets.ModelViewSet):
    queryset = Example.objects.all()
    serializer_class = ExampleSerializer
    permission_classes = [IsAuthenticated]

    def partial_update(self, request, *args, **kwargs):
        item = get_object_or_404(self.queryset, id=kwargs['pk'])
        se = self.get_serializer(item, data=request.data, partial=True)
        se.is_valid(raise_exception=True)
        se.save()
        return Response(se.data)


    def perform_create(self, serializer):
        serializer.save(doctor=self.request.user)
        expertise = Expertise.objects.get(id=self.request.data["expertise"])
        serializer.save(doctor=self.request.user,expertise=expertise)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        # Assuming the `ImagePost` model has a field named `image` that stores the image
        # You can adjust this logic based on your actual model structure

        # Delete the image file from storage (assuming you are using a FileField or ImageField)
        instance.image.delete()

        self.perform_destroy(instance)
        return Response({"message":"example deleted"})

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = serializer.data

        # Include expertise title
        expertise_title = instance.expertise.title if instance.expertise else None
        data['expertise_title'] = expertise_title

        return Response(data)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.queryset.filter(doctor=request.user))
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data

        expertise_ids = [item['expertise'] for item in data if 'expertise' in item]
        expertise_mapping = {expertise.id: expertise.title for expertise in
                             Expertise.objects.filter(id__in=expertise_ids)}

        for item in data:
            expertise_id = item.get('expertise')
            expertise_title = expertise_mapping.get(expertise_id)
            item['expertise_title'] = expertise_title

        return Response(data)


@api_view(["GET", "PUT", "DELETE", "POST"])
@permission_classes([IsAuthenticated, ])
@user_passes_test(lambda u: u.is_active)
def example_list(request, pk=None):
    if request.method == "GET":
        if pk is None:
            example = Example.objects.filter(doctor=request.user).values('id','text','image')
            return Response(example)
        else:
            try:
                example = Example.objects.filter(doctor=request.user).values().get(id=pk)
                return Response(example)
            except:
                return Response({"message": "id not found"})
    elif request.method == "DELETE":
        try:
            example = Example.objects.get(id=pk).delete()
            return Response({"message": "example deleted"})
        except:
            return Response({"message": "id not found"})
    elif request.method == "POST":
        if "title" not in request.POST or "image" not in request.FILES:
            return Response({"message":"enter all fields"})

        try:
            example = Example.objects.create(
                title=request.POST["title"],
                image=request.FILES["image"],
            )
            example.save()
            example.image_url=example.image.url
            if "text" in request.POST:
                example.text = request.POST['text']

            example.save()

            return Response({"message": "example created"})

        except:
            return Response({'message':"example not created (for som reason)"})


    elif request.method == "PUT":
        try:
            example = Example.objects.get(id=pk)
            if "title" in request.POST:
                example.title = request.POST["title"]
            if "text" in request.POST:
                example.text = request.POST["text"]
            if "image" in request.FILES:
                example.image = request.FILES["image"]
                example.save()
                example.image_url=example.image.url
            example.save()
            return Response({"message": "example changed"})
        except:
            return Response({"message": "id not found"})
