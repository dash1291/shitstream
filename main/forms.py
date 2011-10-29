from django import forms
class shitaddform(forms.Form):
	shit_text=forms.CharField(label=u'Text',max_length=200,widget=forms.Textarea)




