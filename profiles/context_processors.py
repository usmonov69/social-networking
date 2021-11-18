from .models import Profile, Relationship


def profile_pic(request):
	if request.user.is_authenticated:
		profile_obj = Profile.objects.get(user=request.user)
		pic = profile_obj.avatar
		return {'picture': pic}
	return {}

def invatation_recevied_no(request):
	if request.user.is_authenticated:
		profile_obj = Profile.objects.get(user=request.user)
		qs_count = Relationship.objectss.invatations_received(profile_obj).count()
		return {"invite_num": qs_count}
	return {}

# def all_profile(request):
# 	if request.user.is_authenticated:
# 		profile_obj = Profile.objects.get(user=request.user)
# 		all_profiles = Profile.objects.get_all_profiles(profile_obj).count()
# 		return {'profile':all_profiles}
# 	return {}