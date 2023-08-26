from rest_framework import serializers
from Company.models import Company,CompanyJobTag, HRDetails,CompanyHiringTag
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

class CompanyJobTagSerializer(serializers.ModelSerializer):
    """ Serializer for the CompanyTag model"""
    class Meta:
        model = CompanyJobTag
        fields = '__all__'


class CompanyHiringTagSerializer(serializers.ModelSerializer):
    """ Serializer for the CompanyTag model"""
    class Meta:
        model = CompanyHiringTag
        fields = '__all__'

class HRDetailsSerializer(serializers.ModelSerializer):
    """ Serializer for the HRDetails model"""
    class Meta:
        model = HRDetails
        fields = ['name', 'email', 'phone_number']

class CompanyAddSerializer(serializers.ModelSerializer):
    """ Serializer for adding a new company to the database"""
    hr_details = HRDetailsSerializer(many=True)

    class Meta:
        model = Company
        fields = ['name', 'about', 'assigned_coordinators', 'salary', 'importance',
                  'years_of_collaboration', 'spoc', 'job_location', 'hr_details',
                  'blacklist', 'job_tags','hiring_tags', 'status']

    # Validating Data
    def validate_name(self, value):
        companies = Company.objects.filter(name=value)
        if companies.exists():
            raise serializers.ValidationError("Company with the same name already exists.")
        return value

    def create(self, validated_data):
        hr_details_data = validated_data.pop('hr_details')
        job_tags_data = validated_data.pop('job_tags')
        hiring_tags_data = validated_data.pop('hiring_tags')
        coordinators_data = validated_data.pop('assigned_coordinators')
        company = Company.objects.create(**validated_data)
        company.assigned_coordinators.set(coordinators_data)
        company.job_tags.set(job_tags_data)
        company.hiring_tags.set(hiring_tags_data)
        for hr_detail_data in hr_details_data:
            hr_detail = HRDetails.objects.create(**hr_detail_data)
            company.hr_details.add(hr_detail)

    
        return company


class CompanyGETSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id','name','salary','job_tags','hiring_tags','importance','years_of_collaboration','blacklist','status']