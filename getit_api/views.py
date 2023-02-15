from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import HowToUse_Serializer, Live_serializer

from getit_api.serializers import Product_Serailizer
from .models import HowToUseDB, LiveDB, Products, Users
# Create your views here.
import jwt
from geopy.geocoders import Nominatim

# Allowed API Endpoints



# class SetLocation(APIView):
#     def post(self,request):
#         try:
#             product_id = request.data['product_id']
#             latitude = request.data['latitude']
#             longitude = request.data['longitude']
#         except:
#             return Response({'status':'required fields - product_id, latitude, longitude'})
#         product = Products.objects.get(id = product_id)
#         product.latitude = latitude
#         product.longitude = longitude
#         product.save()
#         return Response({'status':'ok'})
        



def CheckUser(jwt_token):
    '''
    This function will try to find the user details from that token.
    '''

    # decoding the jwt token
    c_user = jwt.decode(jwt_token,'secret',algorithms='HS256')

    # getting the existing users
    existing_users = Users.objects.all()

    # checking whether the user in the token exist in our database
    '''
    return status:
        success - if user and password are right
        wrong password - if the password is wrong for the particular user
        username not found - if the username entered does not match
    '''
    for user in existing_users:
        if user.username == c_user['username']:
            if user.password == c_user['password']:
                return ({"status":"success","user":user})
            else:
                return ({'status':'wrong password'})
        else:
            return ({'status':'username not found'})

class Sign_up(APIView):
    '''
    This function is will help to create a newuser, it will first validate the data then create the user.
    '''
    def post(self,request):

        # making sure that all the fields are present in the request
        # if not sent response to provide it.
        try:
            username = request.data['username']
            password = request.data['password'] 
            email = request.data['email']
            account_type = request.data['account_type']
            contact_number = request.data['contact_number']
            passion = request.data['passion']
            points = request.data['points']
            subscribers = request.data['subscribers']
            profile_dp = request.data['profile_dp']
        except:
            return Response({'status':'please provide all the fields (username, password, email,contact_number,account_type,passion,points,subscribers,profile_dp)'})


        #validation of the fields

        if len(username) < 5:
            return Response({'status':'username should have atleast 5 charecters'})
        elif len(password) < 8:
            return Response({'status':'password must have atleast 8 charecters'})
        #checking whether a user with the given credentials already exist

        # getting all existing users
        existing_users = Users.objects.all()

        # checking whether the user who is trying to create an account already exist
        # make sure username, email and contact numbers are unique
        for user in existing_users:
            if user.username == username:
                return Response({'status':'username already exist'})
            elif str(user.email) == str(email):
                return Response({'status':'email id already exist'})
            elif str(user.contact_number) == str(contact_number):
                return Response({'status':'contact number already exist'})

        # creating new user in the database
        new_user = Users.objects.create(
                username = username,
                password = password, 
                email = email, 
                account_type = account_type,
                contact_number = contact_number,
                passion = passion,
                points = points,
                subscribers = subscribers,
                profile_dp = profile_dp)

        new_user.save()

        return Response({'status':'success'})


class Login(APIView):
    '''
    This function helps to make the user login after doing the neccessary validation
    '''
    def post(self,request):
        # getting the required data from the request and also validating the fields.
        try:
            username = request.data['username']
            password = str(request.data['password'])
        except:
            return Response({'status':'required fields (username, password)'})        
        #validating
        if len(username) < 5:
            return Response({'status':'username must be 5 charecter'})
        elif len(password) <8 :
            return Response({'status':'password must have atleast 8 charecters'})
        
        #checking for user
        existing_users = Users.objects.all()
        status = 'None'
        for user in existing_users:
            if user.username == username:
                if user.password == password:
                    payload = {
                        'username':username,
                        'password':password
                    }
                    jwt_token = jwt.encode(payload,'secret',algorithm='HS256')
                    response = Response({'status':'success'})
                    response.set_cookie('jwt',jwt_token)
                    return response
                else:
                    status = 'wrong password'
                    break
            else:
                status = 'username not found'
        return Response({'status':status})

class Logout(APIView):
    def get(self,request):
        response = Response({'status':'success'})
        response.delete_cookie('jwt')
        return response

class HomePage(APIView):
    def post(self,request):
        try:
            jwt_token = request.COOKIES.get('jwt')
            result = CheckUser(jwt_token)
            if result['status']=='success':
                return Response({'status':'success',"user":result['user'].username})

        except:
            return Response({'status':'user not logged in','reason':'token not found or invalid token'})


class Product_Handling(APIView):
    '''
    This function helps to add a new product into the database after validaing the neccessary data.
    '''
    def post(self, request):
        user = ''
        # checking for user in jwt and getting the user from it
        try:
            jwt_token = request.COOKIES.get('jwt')
            result = CheckUser(jwt_token)
            if result['status'] == 'success':
                user = result['user']
        except:
            return Response({'status':'user not logged in'})
        # getting the neccessary data from the request 
        try:
            
            name = request.data['name']
            image = request.data['image']
            building_name = request.data['building_name']
            latitude = request.data['latitude']
            longitude = request.data['longitude']
            price = request.data['price']
            description = request.data['description']
        except:
            return Response({'status':'fields required name, builing_name, latitude, longitude, image, price,description)'})

        #validation
        if name == '':
            return Response({'status':'product name cannot be null'})
        elif building_name == '':
            return Response({'status':'building name cannot be null'})
        elif latitude == 0:
            return Response({'status':'latitude cannot be null'})       
            
        elif longitude == 0:
            return Response({'status':'longitude cannot be null'})

        # create new product 
        new_product = Products.objects.create(
            name = name,
            building_name=building_name,
            latitude=latitude,
            longitude=longitude,
            user = user,
            image = image,
            price = price,
            description = description)

        new_product.save()
        return Response({'status':'success'})

    def get(self,request,keyword):
        print(keyword)
        result= []
        products = Products.objects.all()
        for i in products:
            if keyword in i.name:
                result.append(i)
        serialized_products = Product_Serailizer(result,many = True)
        return Response({'status':'success','data':serialized_products.data})



class Search(APIView):
    def get(self,request):
        howtouse  = HowToUseDB.objects.filter(show = True)
        serialized_howtouse = HowToUse_Serializer(howtouse,many=True)
        live = LiveDB.objects.filter(live = True)
        serialzed_live = Live_serializer(live,many=True)
        username = ''
        live = serialzed_live.data
        status = 'ok'
        data = {
            'how to use':serialized_howtouse.data,
            'user':{
                'username':username,
            },
            'live':live,
            
        }
        return Response({'status':status,'data':data})

class HowToUse(APIView):
    def post(self,request):
        try:
            message = request.data['message']
            username = request.data['username']
        except:
            return Response({'status':'message and username fields are neccessary'})

        new_howtouse  = HowToUseDB.objects.create(username = username, message = message)
        new_howtouse.save()
        return Response({'status':'ok'})

    def get(self,request):
        howtouse = HowToUseDB.objects.filter(show=True)
        serialized_howtouse = HowToUse_Serializer(howtouse,many = True)
        return Response({'status':'ok','data':serialized_howtouse.data})

class Live(APIView):
    def post(self,request):
        try:
            username = ''
            title = request.data['title']
            description = request.data['description']
            product_id = request.data['product_id']
            streaming_id = ''
            live = request.data['live_status']
        except:
            return Response({'status':'requires title, description, product_id,live_status'})
        
        try:
            product = Products.objects.get(id = product_id)
        except:
            return Response({'status':'product not found'})

        newlive = LiveDB.objects.create(username = username,title = title,description = description,product = product,streaming_id =streaming_id,live = live)
        newlive.save()
        return Response({'status':'ok'})
    def put(self,request,streaming_id):
        live = LiveDB.objects.get(streaming_id = streaming_id)

class settings(APIView):
    def get(self,request):
        
        return Response({'status':'ok'})