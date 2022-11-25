from django.forms import ModelForm, TextInput, Select, Textarea, NumberInput, FileInput
from dashboard.models import Profile, UsersAreaInfo, Farmer, ProfileAttachments, AreaCrop, FarmerDependents


class FarmerForm(ModelForm):
    class Meta:
        model = Farmer
        fields = [
            'first_name', 
            'last_name', 
            'middle_name',
            'gender',
            'contact_no',
            'tin',
            'philhealth',
            'sss',
            'pagibig',
            'birthdate',
            'civil_status',
            'nationality',
            'spouse',
            'address',
        ]

        widgets = {
            'first_name': TextInput(attrs={
                'class': "form-control",
                'type': "text",
                'placeholder': "Enter farmer firstname",
            }),
            'last_name': TextInput(attrs={
                'class': "form-control",
                'type': "text",
                'placeholder': "Enter farmer lastname",
            }),
            'middle_name': TextInput(attrs={
                'class': "form-control",
                'type': "text",
                'placeholder': "Enter farmer middlename",
            }),
            'gender': Select(attrs={
                'class': "form-control"
            }),
            'contact_no': TextInput(attrs={
                'class': "form-control",
                'type': "tel",
                'placeholder': "XXXX-XXX-XXXX",
            }),
            'birthdate': TextInput(attrs={
                'class': "form-control",
                'placeholder': "mm/dd/yyyy"
            }),
            'civil_status': Select(attrs={
                'class': "form-control"
            }),
            'nationality': TextInput(attrs={
                'class': "form-control",
                'type': "text",
                'placeholder': "Enter farmer nationality",
            }),
            'tin': TextInput(attrs={
                'class': "form-control",
                'type': "text",
                'placeholder': "XXXX-XXX-XXXX",
            }),
            'philhealth': TextInput(attrs={
                'class': "form-control",
                'type': "text",
                'placeholder': "XXXX-XXX-XXXX",
            }),
            'sss': TextInput(attrs={
                'class': "form-control",
                'type': "text",
                'placeholder': "XXXX-XXX-XXXX",
            }),
            'pagibig': TextInput(attrs={
                'class': "form-control",
                'type': "text",
                'placeholder': "XXXX-XXX-XXXX",
            }),
            'spouse': TextInput(attrs={
                'class': "form-control",
                'type': "text",
                'placeholder': "Enter farmer's spouse",
            }),
            'address': Textarea(attrs={
                'class': "form-control",
                'type': "text",
                'rows': "3",
                'placeholder': "Enter address",
            }),
        }


class FarmerAttachmentsForm(ModelForm):
    class Meta:
        model = ProfileAttachments
        fields = [
            'id_picture',
            'cedula',
            'brgy_clearance',
            'tax_dec',
            'valid_id_one',
            'valid_id_two'
        ]

        widgets = {
            'id_picture': FileInput(attrs={
                'class': "custom-file-input",
                'type': "file",
            }),
            'cedula': FileInput(attrs={
                'class': "custom-file-input",
                'type': "file",
            }),
            'brgy_clearance': FileInput(attrs={
                'class': "custom-file-input",
                'type': "file",
            }),
            'tax_dec': FileInput(attrs={
                'class': "custom-file-input",
                'type': "file",
            }),
            'valid_id_one': FileInput(attrs={
                'class': "custom-file-input",
                'type': "file",
            }),
            'valid_id_two': FileInput(attrs={
                'class': "custom-file-input",
                'type': "file",
            }),
            
        }


class UserAreaTechnicalForm(ModelForm):
    class Meta:
        model = UsersAreaInfo
        fields = [
            'farmer_id',
            'total_area',
            'area_coordinates',
            'profile_field',
            'soil_ph',
        ]

        widgets = {
            'farmer_id': Select(attrs={
                'class': "form-control"
            }),
            'total_area': TextInput(attrs={
                'class': "form-control",
                'type': "text",
                'placeholder': "Enter area",
            }),
            'profile_field': TextInput(attrs={
                'class': "form-control",
                'type': "text",
                'placeholder': "Enter profile",
            }),
            'soil_ph': NumberInput(attrs={
                'class': "form-control",
                'type': "text",
                'placeholder': "Enter value",
            }),
        }