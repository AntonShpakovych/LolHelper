from django import forms

REGION =(
    ('BR1','BR1'),
    ('EUN1','EUN1'),
    ('EUW1','EUW1'),
    ('JP1','JP1'),
    ('LA1','LA1'),
    ('LA2','LA2'),
    ('NA1','NA1'),
    ('OC1','OC1'),
    ('RU','RU'),
    ('TR1','TR1'),
)
  
class UsernameForm(forms.Form):
    username = forms.CharField(label='username',max_length=100)
    region = forms.ChoiceField(choices=REGION)