from django.shortcuts import HttpResponse, render, redirect
from django.http import JsonResponse
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from dashboard.models import Farmer, RegionCode, BrgyCode, ProvincialCode, MunCityCode, Profile, UsersAreaInfo, AreaCrop
from dashboard.forms import FarmerForm, FarmerAttachmentsForm, UserAreaTechnicalForm, AreaCropForm
import numpy as np


@login_required(login_url='/auth')
def user_dashboard(request):
    if request.method == 'GET':
        if request.user.is_superuser is not True:
            return HttpResponse('no access')
        else:
            try:
                data_entries = Farmer.objects.all()
                brgy = BrgyCode.objects.filter(muncity_code=settings.DEFAULT_MUNICIPALITY)
                municipality = get_muncity(settings.DEFAULT_MUNICIPALITY)
                province = get_province(settings.DEFAULT_PROVINCE)
                no_of_users = User.objects.all().count()

                default = municipality + ', ' + province

                total_productive_area = UsersAreaInfo.objects.all()
                list_area = []

                if not total_productive_area:
                    mean_area = 0
                else:
                    list_area.clear()
                    for every_area in total_productive_area:
                        list_area.append(every_area.total_area)

                    np_area = np.array([list_area])
                    mean_area = np.mean(np_area)

                context = {
                    'data_entries': data_entries,
                    'mean_area': mean_area,
                    'brgy': brgy,
                    'municipality': default,
                    'no_of_users': no_of_users
                }

                return render(request, 'dashboard/dashboard.html', context)
            except ValueError:
                messages.error(request, 'Something went wrong, please try again later.')
                return redirect('dashboard:user_dashboard')
    else:
        pass


@login_required(login_url='/auth')
def farmers(request):
    if request.method == 'GET':
        farmers = Farmer.objects.all()

        context = {
            'farmers': farmers,
        }

        return render(request, 'dashboard/farmers.html', context)
    else:
        pass


@login_required(login_url='/auth')
def new_farmer(request):
    if request.method == 'GET':
        farmer_form = FarmerForm()
        farmer_attachments = FarmerAttachmentsForm()

        context = {
            'farmer_form': farmer_form,
            'farmer_att': farmer_attachments,
        }
        return render(request, 'dashboard/newfarmer.html', context)
    else:
        try:
            primary_form = FarmerForm(request.POST)
            attachment_form = FarmerAttachmentsForm(request.POST, request.FILES)

            if primary_form.is_valid() and attachment_form.is_valid():
                data = primary_form.save(commit=False)
                data.save()

                attchmnts = attachment_form.save(commit=False)
                farmer = Farmer.objects.get(id=data.id)
                attchmnts.farmer_id = farmer
                attchmnts.save()

                messages.success(request, 'New farmer saved successfully')
                return redirect('dashboard:farmers')
            else:
                messages.error(request, 'Data did not validate. Please try again.')
                return redirect('dashboard:new_farmer')
        except ValueError:
            messages.error(request, 'Something went wrong. Please try again later.')
            return redirect('dashboard:new_farmer')



@login_required(login_url='/auth')
def areas(request):
    if request.method == 'GET':
        data_entries = UsersAreaInfo.objects.all()
        regions = RegionCode.objects.all()

        pa = data_entries
        list_pa = []

        if not pa:
            productive_area = 0
        else:
            list_pa.clear()
            for area in pa:
                list_pa.append(area.total_area)

            np_pa = np.array([list_pa])
            productive_area = np.sum(np_pa)

        context = {
            'areas': data_entries,
            'productive_area': productive_area,
            'regions': regions,
        }

        return render(request, 'dashboard/areas.html', context)
    else:
        pass


@login_required(login_url='/auth')
def new_area(request):
    if request.method == 'GET':
        brgy = BrgyCode.objects.filter(muncity_code=settings.DEFAULT_MUNICIPALITY)
        form = UserAreaTechnicalForm()

        context = {
            'brgy': brgy,
            'form': form,
        }
        return render(request, 'dashboard/newarea.html', context)
    else:
        try:
            entry_form = UserAreaTechnicalForm(request.POST, request.FILES)

            if entry_form.is_valid():
                save_entry = entry_form.save(commit=False)
                save_entry.brgy = str(request.POST.get('brgy'))
                save_entry.save()
            else:
                raise ValueError

            form_crop = AreaCropForm()

            context = {
                'area_id': save_entry.id,
                'form_crop': form_crop,
            }

            return render(request, 'dashboard/crop.html', context)

        except ValueError:
            messages.error(request, "Error loading data. Please try again.")
            return redirect('dashboard:new_area')

@login_required(login_url='/auth')
def add_crop(request):
    if request.method == 'POST':
        try:
            form = AreaCropForm(request.POST)

            if form.is_valid():
                new_area = form.save(commit=False)

                area = request.POST['area']
                area_id = UsersAreaInfo.objects.get(id=area)
                new_area.area_id = area_id

                new_area.save()

                crops = list(AreaCrop.objects.filter(area_id=area_id).values())
            

                return JsonResponse(data=crops, safe=False)
        except ValueError:
            messages.error(request, 'Data entry encountered an error. Please try again.')
            return redirect('dashboard:new_area')

# User Defined Functions

def get_region(region_id):
    if region_id != 0:
        region_name = RegionCode.objects.filter(reg_code=region_id).region_name
        return region_name


def get_province(province_id):
    if province_id != 0:
        province_name = ProvincialCode.objects.get(prov_code=province_id).province_name
        return province_name


def get_muncity(muncity_id):
    if muncity_id != 0:
        muncity_name = MunCityCode.objects.get(muncity_code=muncity_id).muncity_name
        return muncity_name


def get_brgy(brgy_id):
    if brgy_id != 0:
        brgy_name = BrgyCode.objects.get(brgy_psgc_code=brgy_id).brgy_name
        return brgy_name