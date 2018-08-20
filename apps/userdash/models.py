from django.db import models
from django.core.validators import validate_email
import datetime , bcrypt, re
NAME_REGEX = re.compile(r'^[a-zA-Z ]+$')
#  add models
class UserManager(models.Manager):
    def regValidator(self, postData):
        result = {'errors':[]}
        if len(postData['first_name']) <1:
            result['errors'].append("First Name too short")
        if len(postData['last_name']) <1:
            result['errors'].append("Last Name too short")
        if len(postData['email']) <1:
            result['errors'].append("Email too short")
        if len(postData['password']) <8:
            result['errors'].append("Password too short")
        if postData['password'] !=postData['confirm_password']:
            result['errors'].append("Passwords do not match")
        try:
            if not NAME_REGEX.match(postData['first_name']) or not NAME_REGEX.match(postData['last_name']):
                result['errors'].append("Name fields can only be english letters")
        except:
            pass
        try:
            validate_email(postData['email'])
        except:
            result['errors'].append("Invalid email")
        throwaway = User.objects.filter(email = postData['email'])
        if len(throwaway)> 0:
            result['errors'].append("Please use another email")
        if len(result['errors'])> 0:
            print("errors found, escaping now...")
            return result
# ******************************** VALIDATION PASS *************************************
        print("regValidator Pass")
        hash1 = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
        hash1= hash1.decode()
        all_users= User.objects.all()
        if len(all_users) ==0:
            user_level = 9
        else:
            user_level = 1
        newUser = User.objects.create(
            first_name = postData['first_name'],
            last_name = postData['last_name'],
            email = postData['email'],
            password = hash1,
            user_level = user_level,
        )
        result['user_id'] = newUser.id
        return result

    def loginValidator(self, postData):
        result = {'errors':[]}
        throwaway = User.objects.filter(email = postData['email'])
        if len(throwaway) > 0:
            if bcrypt.checkpw(postData['password'].encode(),throwaway[0].password.encode() ):
                result['user_id'] = throwaway[0].id
                return result
        result['errors'].append("Password or Email did not match")
        return result

    def updateValidator(self, postData):
        result = {'errors':[]}
        throwaway = User.objects.get(id = postData['edit_id'])
        if 'description' in postData:
            throwaway.description = postData['description']
        if 'password' in postData:
            if len(postData['password']) <8:
                result['errors'].append("Password too short")
            if postData['password'] !=postData['confirm_password']:
                result['errors'].append("Passwords do not match")
            if len(result['errors'])> 0:
                print("errors found, escaping now...")
                return result
            hash1 = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
            hash1= hash1.decode()
            throwaway.password= hash1 
            result['errors'].append("Password succesfully changed")
# update name , email ,user_level
        if 'first_name' in postData:
            if len(postData['first_name']) <1 or len(postData['last_name']) <1:
                result['errors'].append("Name too short")
            if len(postData['email']) <1:
                result['errors'].append("Email too short")
            if not NAME_REGEX.match(postData['first_name']) or not NAME_REGEX.match(postData['last_name']):
                result['errors'].append("Name fields can only be english letters")
            try:
                validate_email(postData['email'])
            except:
                result['errors'].append("Invalid email")
            if len(result['errors'])> 0:
                print("errors found, escaping now...")
                return result
            throwaway.first_name= postData['first_name']
            throwaway.last_name= postData['last_name']
            throwaway.email= postData['email']
            if 'user_level' in postData:
                newlevel = 1
                if postData['user_level'] == "Admin":
                    newlevel= 9
                if throwaway.user_level != newlevel:
                    result['errors'].append(("Changed access for "+ throwaway.first_name + " " +throwaway.last_name))
                throwaway.user_level= newlevel
        throwaway.save()
        return result


class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    user_level = models.IntegerField(default=1, blank=True, null=True)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    create_d = models.DateTimeField(auto_now_add = True)
    update_d = models.DateTimeField(auto_now = True)
    description = models.CharField(max_length=255,null=True, blank=True)
    objects = UserManager()


class Message(models.Model):
    content = models.CharField(max_length = 255)
    owner = models.ForeignKey(User, related_name ="owner" , on_delete = models.CASCADE)
    author = models.ForeignKey(User, related_name = "author" , on_delete = models.CASCADE)
    create_d = models.DateTimeField(auto_now_add = True)

class Comment(models.Model):
    content = models.CharField(max_length = 255)
    message = models.ForeignKey(Message, related_name ="comments", on_delete = models.CASCADE)
    author = models.ForeignKey(User, related_name ="comments", on_delete = models.CASCADE)
    create_d = models.DateTimeField(auto_now_add = True)

