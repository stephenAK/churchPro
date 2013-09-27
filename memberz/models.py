from django.db import models
from datetime import datetime,date,time
from django.contrib import admin
from countries.models import Country

#MEMBERS TABLE
class Year(models.Model):
      	year		=	models.PositiveIntegerField(unique =True,blank=False, null = False)
        date_added	= 	models.DateTimeField (auto_now_add=True, blank =True, null = True)
     	date_updated    = 	models.DateTimeField (auto_now=True,blank =True, null = True) 
	
	def __unicode__(self):
               return '%s'%(self.year)

	
	class Meta:
		verbose_name 	    = "YEAR"
		verbose_name_plural = "YEARS"



class Halls(models.Model):
       	name		=	models.CharField(max_length=40, blank=False, null = False,help_text="Please enter name of Hall")
        short_desp 	=	models.TextField("Short Description",blank=True, null=True, help_text="Can be left blank")
        date_added	= 	models.DateTimeField (auto_now_add=True, blank =True, null = True)
     	date_updated    = 	models.DateTimeField (auto_now=True,blank =True, null = True)   
	
	def __unicode__(self):
               return self.name

        def hall_name(self):
            return "Click to edit -> %s"%(self.name.upper())
	
	class Meta:
		verbose_name 	    = "HALL"
		verbose_name_plural = "HALLS"

class Auxillary(models.Model):
       	name		=	models.CharField(max_length="50",blank=False, null = False, help_text="Please enter Auxilliary Name")
      	short_desp 	=	models.TextField("Short Description",blank=True, null=True, help_text="Can be left blank")
        date_added	= 	models.DateTimeField (auto_now_add=True, blank =True, null = True)
     	date_updated    = 	models.DateTimeField (auto_now=True,blank =True, null = True)  
	
	def __unicode__(self):
               return self.name	

	class Meta:
		verbose_name 	    = "AUXILLARY"
		verbose_name_plural = "AUXILLARIES"

class Position(models.Model):
        title		=	models.CharField(max_length=50, blank=False, null =False, help_text="Please enter the title of the Position")
        short_desp 	=	models.TextField("Short Description",blank=True, null=True, help_text="Can be left blank")
        date_added	= 	models.DateTimeField (auto_now_add=True, blank =True, null = True)
     	date_updated    = 	models.DateTimeField (auto_now=True,blank =True, null = True) 

	def __unicode__(self):
               return self.title
	
	class Meta:
		verbose_name 	    = "POSITION"
		verbose_name_plural = "POSITIONS"

class member(models.Model):
        mem_id		=	models.CharField("Member ID",blank= True, null=True,max_length=30,unique =True, help_text="Generated Automatically on first save")
	index_number	=	models.CharField("Student's ID",max_length=30,unique=True, blank=True, null=True, help_text="Please enter Student's ID number")
	surname		=	models.CharField(max_length = 40, blank=False, help_text = "Please Enter Member's Surname",null= False)
      	other_name	=	models.CharField("Other name(s)",max_length = 100, blank=False, null=False, help_text="Please Enter Member's Surname")
      	phone_number	=	models.CharField(max_length=15,unique = True,blank=True, null = True, default = "",help_text= "Please enter Member's Phone Number")
      	email_addres	=	models.EmailField("Email-Address", blank=True, null = True,help_text="Please enter Member's Email-address")
	age             =	models.PositiveIntegerField(blank = True, null = True,help_text ="Generated from date of birth")
     	sex             =	models.CharField('Gender', choices =(("Male","Male"),("Female","Female")),max_length = 7)
     	date_Of_birth   =	models.DateField(blank = True, null = True,help_text = "YYYY-MM-DD")
        level           =	models.CharField(max_length=3,blank =True, null = True,default = "None",choices=(("100","100"),("200","200"),("300","300"),("400","400")))
        course		=	models.CharField(max_length=60,blank=True, null = True)	
        country		=	models.ForeignKey(Country,default = "GH")
        year            =       models.ForeignKey(Year,default =None, blank =True, null = True,help_text="Select Year of completion/ enter new if not in the list")
	hall		=	models.ForeignKey(Halls,blank =True, null = True)
	auxilliary	=	models.ForeignKey(Auxillary,help_text ="Select Member's Auxilliary/ enter new if not in the list",blank=True, null=True)
	current_position=	models.ForeignKey(Position, related_name="c_position", blank= True, null = True,
				help_text="Select Member's Position in the church, leave blank if member hold's no position")
        positions_held  =       models.ManyToManyField(Position, verbose_name ="positions held",related_name="post_held",blank=True, null=True)
        completed       =       models.BooleanField(blank = False, null = False,help_text = "Check if person has completed ")
	date_added	= 	models.DateTimeField (auto_now_add=True, blank =True, null = True)
     	date_updated    = 	models.DateTimeField (auto_now=True,blank =True, null = True)
	
        def __unicode__(self):
            return '%s, %s'%(self.surname,self.other_name)
        
	def Full_name (self):
              return "%s, %s" %(self.surname, self.other_name)

        def completed_(self):
             if self.completed == True:
			return "YES"
             else:
                        return "NO"
        def birthday(self):
            if self.date_Of_birth:
                   if int(self.date_Of_birth.strftime("%G")-int(self.datetime.now().strftime("%G%")))==0:
                           return "Birth day is due"
                   else:
                           pass
        def member_id(self):
              self.mem_id = "NUBS0%s"%(self.pk)
              return self.mem_id
	
	def Age(self):
		if self.date_Of_birth:
	                 min_allowed_dob = datetime(1900,01,01)
	         	 max_allowed_dob = datetime.now()
			 if int(self.date_Of_birth.strftime("%G")) >= int( min_allowed_dob.strftime("%G") ) and int(self.date_Of_birth.strftime("%G")) <= int(max_allowed_dob.strftime("%G")):
               			 self.age  = "%s" %(int(max_allowed_dob.strftime("%G"))-  int(self.date_Of_birth.strftime("%G")) )
               			 return "%s" %(self.age)
                             
			 else:
				 return "Invalid Date"
          	elif self.age and int(self.age[0:3])<=120:
	        	self.date_Of_birth = None
		        return True	
	
	
        def save(self,*args,**kwargs):
		self.member_id() 
                self.Age()
    		super(member,self).save(*args, **kwargs)
		return True 
	
	class Meta:
		verbose_name 	    = "MEMBER"
		verbose_name_plural = "MEMBERS"


class tithe(models.Model):
       	amount		=	models.PositiveIntegerField("Amount",blank=True,null =True,help_text="Please enter amount (GHS)")
       	tither 		=	models.ForeignKey(member,verbose_name ="Member",related_name ="tith")
	date_paid	=	models.DateField(default = datetime.now(),help_text="Select date of tithe payment", blank =True, null = True)
	date_added	= 	models.DateTimeField (auto_now_add=True, blank =True, null = True)
     	date_updated    = 	models.DateTimeField (auto_now=True,blank =True, null = True)

	def __unicode__(self):
            return 'Tithe by %s, %s '%(self.tither.surname,self.tither.other_name)

	class Meta:
		verbose_name 	    = "TITHE"
		verbose_name_plural = "TITHES"


                   
class titheInline(admin.TabularInline):
      model = tithe

class member_Admin(admin.ModelAdmin):
      list_display = (	'member_id',
			'index_number','Full_name',
			'sex','phone_number',
			'email_addres','age',
			'hall','date_Of_birth',
			'level','course','year','completed_'
			)
      search_fields = ('index_number','surname','other_name','phone_number')
      list_filter = ('sex','hall','level')
      list_per_page = 50
      date_hierarchy    = 'date_added'
      inlines = [titheInline]
      readonly_fields =('age','mem_id',)
      fieldsets         = ( ("Personal details", {'fields':
							('index_number',('surname','other_name'),
							'sex',('phone_number','email_addres'),
							('date_Of_birth','age'),
							('level','hall'),'course')}),
                             ("Church details",{'fields':('mem_id',('auxilliary','current_position'),'positions_held',('year','completed'))}),      )

admin.site.register(member, member_Admin)
admin.site.register(Halls)
admin.site.register(Year)
admin.site.register(Position)
admin.site.register(Auxillary)
admin.site.register(tithe)








