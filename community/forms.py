from django import forms
from PIL import Image
from io import BytesIO
from .models import article, Category
from .models import CommunityComment
 
class RegisterForm(forms.ModelForm):

    category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label=None)
    
    class Meta:
        model = article
        fields = ['article_name', 'description', 'category', 'article_img']
        

    def clean_image(self):
        image = self.cleaned_data.get('article_img')
        if image:
            # 이미지 사이즈 조정
            max_size = (500, 500)
            img = Image.open(BytesIO(image.read()))
            img.thumbnail(max_size)
            img_format = img.format.lower()
            if img_format not in ['jpeg', 'jpg', 'png']:
                raise forms.ValidationError("올바른 이미지 포맷이 아닙니다. JPEG 또는 PNG 형식을 사용하세요.")
            return image
        else:
            raise forms.ValidationError("이미지를 업로드하세요.")

#===댓글


class CommentForm(forms.ModelForm):
    class Meta:
        model = CommunityComment
        fields = ['content']

class CommentEditForm(forms.ModelForm):
    class Meta:
        model = CommunityComment
        fields = ['content']
