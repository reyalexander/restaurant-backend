from django.db import models
from apps.resource.models import Resource
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class Role(models.Model):
    ADMINISTRATOR = 1
    ADMINISTRATIVE = 2
    WORKER = 3

    ROLE_CHOICES = (
        (ADMINISTRATOR, 'Administrator'),
        (ADMINISTRATIVE, 'Administrative'),
        (WORKER, 'Worker'),
    )

    STATUS_CHOICES = (
        (1, 'Activo'),
        (2, 'Inactivo'),
        (3, 'Eliminado'),
    )

    name = models.CharField(max_length=100, choices=ROLE_CHOICES, unique=True)
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.get_name_display()

class Permission(models.Model): 
    CREATE = 1
    UPDATE = 2
    READ = 3
    DELETE = 4

    PERMISSION_CHOICES = (
        (CREATE, 'Create'),
        (UPDATE, 'Update'),
        (READ, 'Read'),
        (DELETE, 'Delete'),
    )

    STATUS_CHOICES = (
        (1, 'Activo'),
        (2, 'Inactivo'),
        (3, 'Eliminado'),
    )

    name = models.CharField(max_length=100, choices=PERMISSION_CHOICES, unique=True)
    id_rol = models.ForeignKey(Role, on_delete=models.CASCADE ,related_name='role')
    id_resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name='resource')
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.get_name_display()
    

class UserManager(BaseUserManager):
    '''Interfaz que proporcionan las operaciones de consulta de la base de datos para Usuarios'''
    def create_user(self, email, first_name, last_name, password):
        '''función para crear usuarios'''
        if not email: raise ValueError('falta el correo electrónico')
        user = self.model(email=self.normalize_email(email),first_name=first_name,last_name=last_name)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, first_name, last_name, password):
        '''función para crear un super usuario (comando: createsuperuser)'''
        user = self.create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    STATUS_CHOICES = (
        (1, 'Activo'),
        (2, 'Inactivo'),
        (3, 'Eliminado'),
    )

    id_role = models.ForeignKey(Role,on_delete=models.SET_NULL,null=True,blank=True,verbose_name='rol')
    email = models.EmailField(blank=False,unique=True,max_length=32,verbose_name='correo electrónico') # correo institucional único por usuario
    first_name = models.CharField(blank=False,max_length=32,verbose_name='nombres') # nombres completos
    last_name = models.CharField(blank=False,max_length=32,verbose_name='apellidos') # apellidos completos
    ruc = models.CharField(blank=False,max_length=11,verbose_name='RUC') # RUC
    photo = models.ImageField(upload_to="photo_user",null=True,blank=True,verbose_name='foto de perfil',) # foto de perfil del usuario
    is_admin = models.BooleanField(blank=True,default=False,verbose_name='super administrador')
    # estado de super administrador del usuario
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False,verbose_name='super usuario')
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=1)
    # estado del usuario
    created = models.DateTimeField(auto_now_add=True,verbose_name='fecha de creación')
    updated = models.DateTimeField(auto_now=True,verbose_name='fecha de actualización')
    deleted = models.BooleanField(default=False, null=True)
    dark_mode = models.BooleanField(default=False, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name']

    class Meta:
        verbose_name = 'usuario'
        verbose_name_plural = 'usuarios'
        ordering = ['first_name']

    def __str__(self): return f'{self.first_name} {self.last_name}'

