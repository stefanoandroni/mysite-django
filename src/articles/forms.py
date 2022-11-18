from .models import Article, Comment

from django import forms

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("content",)
        widgets = {
          'content': forms.Textarea(attrs={'rows':4, 'class': 'form-control'}),
        }

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ("title", "topic", "summary_text", "content", "image")
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            new_attrs = {
                'class': 'form-control',
            }
            self.fields[field].widget.attrs.update(new_attrs) 
        self.fields['summary_text'].widget.attrs.update({"rows": 3}) 
        self.fields['content'].widget.attrs.update({"rows": 25}) 

    

