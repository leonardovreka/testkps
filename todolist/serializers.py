from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import Todo

#imports για το registration
from django.contrib.auth.models import User
from django.contrib.auth import password_validation

class TodoSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source="owner.username")

    class Meta:
        model = Todo
        fields = [
            'id',
            'name',
            'title',
            'description',
            'is_completed',
            'due_date',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'name', 'created_at', 'updated_at']

#registration
class RegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    email = serializers.EmailField(                                                      #Το γράφω εδώ γτ θέλω να το τσεκάρω κατευθείαν στo field level. Και το
        required=True,                                                                   #django κάνει provide δικό του checker (UniqueValidator)
        validators=[UniqueValidator(queryset=User.objects.all())]                        #αλλιώς θα μπορούσα να το τσεκάρω όπως στο pass manually
    )
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)  #write_only: only input not api response
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True) #style: drf input box named password

                                                                                         # πρέπει να είναι ονομασμένο meta
    class Meta:
        model = User
        fields = ["username", "email", "password", "password2"]

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:                                      #σε αντίθεση με το email εδώ κάνω object level validation οχι field
            raise serializers.ValidationError("Passwords don't match")                   #γιατί μπορώ να κάνω validate διάφορα field μεταξύ τους πχ emal != name
        password_validation.validate_password(attrs['password'])                         #djangos built in validator checks for numeric only etc.
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')                                                  #.pop το αφαιρεί απο το DB γτ θέλουμε μόνο το 1 απο τα 2
        password = validated_data.pop('password')                                        #το περνάει στο variable και μετά το αφαιρεί
        user = User(**validated_data)                                                    #φτιάχνει το νεο user με τα 2 απομείναντα fields
        user.set_password(password)                                                      #κάνει hash το pass πριν το κάνει save
        user.save()
        return user
