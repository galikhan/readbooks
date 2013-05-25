from django.db import models
import datetime

class QuizList(models.Model):

    name = models.CharField( max_length = 255 )
    number_of_questions = models.IntegerField(default=0)
    user = models.IntegerField()
    create_date = models.DateTimeField( default=datetime.datetime.now() )
    #time when user finished quiz added all quistions fully
    #set at the end

    def __unicode__(self):
        return self.name


class QuestionCart(models.Model):
    quiz_list = models.ForeignKey(QuizList)
    question = models.IntegerField()


class SbTopicsList(models.Model):

    quarter = models.IntegerField(db_column="id_quarter")
    class_field = models.ForeignKey("SbClass", db_column = "id_class")
    branch = models.IntegerField(db_column="id_branch")
    topic = models.CharField(max_length=255L)
    subtopic = models.CharField(max_length=255L)
    description = models.CharField(max_length=30L)

    class Meta:
        db_table = 'sb_topics_list'

    def __unicode__(self):
        return self.subtopic

class SbSubtopicsList(models.Model):

    topic = models.ForeignKey("SbTopicsList")
    name = models.CharField(max_length=255L)
    number_of_questions = models.IntegerField()
    #add number of questions field#
    #add operation # when user inserts new value with this subtopic increment value +1
    #delete operation # when user delete question then increase for -1

    class Meta:
        db_table = 'sb_subtopics_list'

    def __unicode__(self):
        return self.name


class SbClass(models.Model):
    name = models.CharField(max_length=20L)
    number_view = models.IntegerField()
    class Meta:
        db_table = 'sb_class'



class SbQuestions(models.Model):

    year_id = models.IntegerField()
    grade_id = models.IntegerField()
    teacher_id = models.IntegerField()
    d_q_type = models.ForeignKey("SbQuestionType")
    d_topic_id = models.IntegerField()
    d_subtopic_id = models.IntegerField()
    q_complexity_id = models.IntegerField()
    id_q_lang = models.IntegerField(null=True, blank=True)
    question = models.TextField()
    solution = models.TextField()
    image = models.CharField(max_length=255L, blank=True)
    image_location = models.CharField(max_length=5L)
    date_filled = models.DateTimeField()
    id_en_language_level = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = 'sb_questions'


class SbVariants(models.Model):

    question = models.ForeignKey("SbQuestions")
    name = models.TextField(blank=True)

#    def __unicode__(self):
#        return self.question 

    class Meta:
        db_table = 'sb_variants'


class SbQuestionMappings(models.Model):

    question = models.ForeignKey("SbQuestions")
    key_value = models.CharField(max_length=45L, blank=True)
    wrong_value = models.CharField(max_length=45L, blank=True)
    right_value = models.CharField(max_length=45L, blank=True)
    class Meta:
        db_table = 'sb_question_mappings'


class SbAnswers(models.Model):
    
    question = models.ForeignKey("SbQuestions")
    variant_id = models.IntegerField(null=True, blank=True)
    name = models.TextField(blank=True)
    view_order = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = 'sb_answers'


class SbViewOrder(models.Model):

    name = models.IntegerField(null=True, blank=True)
    letter = models.CharField(max_length=1L, blank=True)
    class Meta:
        db_table = 'sb_view_order'


class SbQuestionType(models.Model):
    name = models.CharField(max_length=45L, blank=True)
    kz_name = models.CharField(max_length=30L)
    tr_name = models.CharField(max_length=30L)
    short_name = models.CharField(max_length=25L, blank=True)
    number_value = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = 'sb_question_type'

    def __unicode__(self):
        return self.name







###
"""
class SbQuestionCounter(models.Model):
    id = models.IntegerField(primary_key=True)
    branch_id = models.IntegerField()
    year_id = models.IntegerField()
    amount = models.IntegerField()
    class Meta:
        db_table = 'sb_question_counter'

class SbExam(models.Model):
    name = models.CharField(max_length=150L, blank=True)
    short_name = models.CharField(max_length=45L, blank=True)
    class Meta:
        db_table = 'sb_exam'

class SbQuestionComplexity(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=15L, blank=True)
    kz_name = models.CharField(max_length=8L)
    tr_name = models.CharField(max_length=8L)
    short_name = models.CharField(max_length=5L, blank=True)
    number = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = 'sb_question_complexity'

class SbQuestionLanguage(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30L)
    short_name = models.CharField(max_length=10L)
    class Meta:
        db_table = 'sb_question_language'



class SbQuizConfiguration(models.Model):
    id = models.IntegerField(primary_key=True)
    teacher_id = models.IntegerField(null=True, blank=True)
    grade_id = models.IntegerField(null=True, blank=True)
    exam_id = models.IntegerField(null=True, blank=True)
    topic_id = models.IntegerField(null=True, blank=True)
    subtopic_id = models.IntegerField(null=True, blank=True)
    single_answer = models.IntegerField(null=True, blank=True)
    multiple_answer = models.IntegerField(null=True, blank=True)
    fill_in_blanks = models.IntegerField(null=True, blank=True)
    true_false = models.IntegerField(null=True, blank=True)
    classic = models.IntegerField(null=True, blank=True)
    olympiad = models.IntegerField(null=True, blank=True)
    match_words = models.IntegerField(null=True, blank=True)
    class Meta:
        db_table = 'sb_quiz_configuration'

class SbQuizList(models.Model):
    id = models.IntegerField(primary_key=True)
    user_id = models.IntegerField()
    name = models.CharField(max_length=255L)
    duration = models.IntegerField()
    variant_id = models.IntegerField()
    number_of_questions = models.IntegerField()
    create_date = models.DateTimeField()
    class Meta:
        db_table = 'sb_quiz_list'

class SbQuizMixedVariants(models.Model):
    id = models.IntegerField(primary_key=True)
    quiz_list_id = models.IntegerField()
    question_id = models.IntegerField()
    variant_ids = models.TextField()
    class Meta:
        db_table = 'sb_quiz_mixed_variants'

class SbQuizQuestions(models.Model):

    id_quiz_list = models.IntegerField()
    id_questions = models.IntegerField()
    class Meta:
        db_table = 'sb_quiz_questions'

class SbQuizVariants(models.Model):
    id = models.IntegerField(primary_key=True)
    quiz_list_id = models.IntegerField()
    question_ids = models.TextField()
    filename = models.CharField(max_length=50L)
    fontsize = models.IntegerField()
    column_number = models.IntegerField()
    class Meta:
        db_table = 'sb_quiz_variants'





"""