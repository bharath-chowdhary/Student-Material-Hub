from django.forms import ModelForm
from .models import Admin,Section,Subject,Document
from django.core.exceptions import ValidationError
class Adminform(ModelForm):
    class Meta:
        model=Admin
        fields=['name','email','section']

    def clean_name(self):
        data=self.cleaned_data['name']
        if not data.isalnum() or not any(c.isalpha() for c in data):
            raise ValidationError(f'Enter Only Characters Ex: a,b,c')
        
        data=data.strip().lower()
        duplicates=Admin.objects.filter(name=data).exists()
        if duplicates:
            raise ValidationError(f'The Username Already Exists')
        return data

    def clean_email(self):
        mail=self.cleaned_data['email']
        dups=Admin.objects.filter(email=mail.lower()).exists()
        if dups:
            raise ValidationError(f'The Mail ID is Already Exist')
        if not mail.endswith('@qiscet.edu.in'):
            raise ValidationError(f'This is not recognized College Mail ID')
        return mail.lower()

    def clean(self):
        cleaned_data=super().clean()

        se=cleaned_data.get('section')
        mail=cleaned_data.get('email')

        data=''
        flag=False

        # SAME LOGIC AS FRIEND
        if not se or not mail:
            return cleaned_data

        for i in se:
            if i!=' ':
                data+=i

            if i.isdigit():
                flag=True

        if not flag or '-' not in se:
            raise ValidationError(
                f'This is not Reconigsed as Section, Example: CSE-1'
            )

        batch='20'
        if mail:
            batch='20'+mail[:2]

        Section.objects.get_or_create(
            name=data,
            batch=batch
        )

        data+=f'[{batch}]'

        cleaned_data['section']=data.upper()

        count=Admin.objects.filter(
            section=cleaned_data['section']
        ).count()

        if count>=5:
            raise ValidationError(
                f'Registraion Are Limited Only For 5 Students in {se}!'
            )

        return cleaned_data
class SubjectForm(ModelForm):
    class Meta:
        model=Subject
        fields=['name']
    def __init__(self,*args,**kwargs):
        self.user=kwargs.pop('user',None)
        super().__init__(*args,**kwargs)
    def save(self, commit = True):
        subject=super().save(commit=False)  #subject.name = "Python",subject.section = ???
        if self.user:
            admin=Admin.objects.filter(name=self.user).first()
            if not admin:
                raise ValidationError(f'Unable to Add Subject because of Username is not Admin or Invalid!')
            sec=Section.objects.filter(name=admin.section[:-6], #"CSE-1[2024]"
            batch=admin.section[-5:len(admin.section)-1]).first()
            if not sec:
                raise ValidationError(f'Unable to Add Subject, The Username Is not Admin or Invalid!')
            sub = Subject.objects.filter(name=subject.name,section=sec)
            if sub.exists():raise ValidationError(f'Subject Already Exists in this Section!')
            subject.section=sec         #name=Python,section  = CSE-1     commit becomes True 
        else:
            raise ValidationError(f'Unable to add Subject,The Username is Invalid!')
        if commit:subject.save()
        return subject

class MaterialForm(ModelForm):
    class Meta:
        model=Document
        fields=['name','file']
    def __init__(self,*args,**kwargs):
        self.subject=kwargs.pop('subject',None)#Gets the value of subject Removes subject from kwargs
        super().__init__(*args,**kwargs)
    def save(self,commit=True):
        materiall=super().save(commit=False)
        data=self.subject #Python[CSE-1(2025)]
        i,n=data.index('[')+1,len(data)-1  #i to get section name combined with batch
        sname=data[i:n] #"CSE-1(2025)"
        sn=sname[:-6]  #extracting section name "CSE-1"
        sb = int(sname[-6:][1:-1]) #extracting batch "2025"
        sec=Section.objects.get(name=sn,batch=sb) #Now Django searches the Section table.
        sub = Subject.objects.filter(name=data[:i-1],section=sec).first()  # data[:i-1]="Python"  Find the "Python" subject belonging to the CSE-1 2025 section.
        materiall.subject=sub  # You are Connected the Material to the Particular Subject
        print(data)  #Just print in terminal #Python[CSE-1(2025)]
        if commit:materiall.save()
        return materiall
