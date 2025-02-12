from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.password_validation import validate_password

User = get_user_model()


# Ro'yxatdan o'tish (oddiy yoki superuser)
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    is_superuser = serializers.BooleanField(write_only=True, default=False)  # Superuser tanlash imkoniyati

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name', 'last_name', 'is_superuser')

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Ushbu foydalanuvchi nomi allaqachon mavjud.")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Ushbu email allaqachon ishlatilgan.")
        return value

    def create(self, validated_data):
        is_superuser = validated_data.pop('is_superuser', False)  # Superuser bo‘lishi tekshiriladi
        password = validated_data.pop('password')  # Parolni ajratib olish

        if is_superuser:
            user = User.objects.create_superuser(**validated_data)  # Superuser yaratish
        else:
            user = User.objects.create_user(**validated_data)  # Oddiy user yaratish

        user.set_password(password)  # Parolni xavfsiz saqlash
        user.save()
        return user


# Login qilish
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(username=data.get('username'), password=data.get('password'))
        if user is None:
            raise serializers.ValidationError("Foydalanuvchi nomi yoki parol noto'g'ri.")
        if not user.is_active:
            raise serializers.ValidationError("Foydalanuvchi bloklangan.")
        data['user'] = user  # Authtoken yoki JWT uchun
        return data


# Parolni o'zgartirish
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, validators=[validate_password])

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Eski parol noto'g'ri.")
        return value

    def save(self, **kwargs):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user


# Profilni ko'rish
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'is_superuser')


# Profilni tahrirlash
class ProfileEditSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

    def validate_email(self, value):
        user_id = self.instance.id if self.instance else None
        if User.objects.exclude(id=user_id).filter(email=value).exists():
            raise serializers.ValidationError("Ushbu email allaqachon ishlatilgan.")
        return value
