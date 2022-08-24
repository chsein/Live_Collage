from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView
import pandas as pd

class AboutView(TemplateView):
    template_name = "collageapp/1.html"


    collage = pd.read_csv('collageapp/csv/collage.csv')


    def get_context_data(self, **kwargs):
        context = super(AboutView, self).get_context_data(**kwargs)

        if len(self.collage) >=1:
          context['one_title'] = self.collage['article_title'][0]
          context['one_content'] = self.collage['article_summary'][0]
          context['one_link'] = self.collage['article_link'][0]
          context['one_keyword'] = self.collage['keyword'][0]
          context['one_left'] = self.collage['img_x'][0]
          context['one_top'] = self.collage['img_y'][0]
          context['one_image'] = self.collage['img'][0]
          context['one_newsimage'] = self.collage['img_article'][0]
          context['time'] = self.collage['time'][0]


        if len(self.collage) >=2:
          context['two_title'] = self.collage['article_title'][1]
          context['two_content'] = self.collage['article_summary'][1]
          context['two_link'] = self.collage['article_link'][1]
          context['two_keyword'] = self.collage['keyword'][1]
          context['two_left'] = self.collage['img_x'][1]
          context['two_top'] = self.collage['img_y'][1]
          context['two_image'] = self.collage['img'][1]
          context['two_newsimage'] = self.collage['img_article'][1]


        if len(self.collage) >=3:
          context['three_title'] = self.collage['article_title'][2]
          context['three_content'] = self.collage['article_summary'][2]
          context['three_link'] = self.collage['article_link'][2]
          context['three_keyword'] = self.collage['keyword'][2]
          context['three_left'] = self.collage['img_x'][2]
          context['three_top'] = self.collage['img_y'][2]
          context['three_image'] = self.collage['img'][2]
          context['three_newsimage'] = self.collage['img_article'][2]

        if len(self.collage) >=4:
          context['four_title'] = self.collage['article_title'][3]
          context['four_content'] = self.collage['article_summary'][3]
          context['four_link'] = self.collage['article_link'][3]
          context['four_keyword'] = self.collage['keyword'][3]
          context['four_left'] = self.collage['img_x'][3]
          context['four_top'] = self.collage['img_y'][3]
          context['four_image'] = self.collage['img'][3]
          context['four_newsimage'] = self.collage['img_article'][3]


        if len(self.collage) >=5:
          context['five_title'] = self.collage['article_title'][4]
          context['five_content'] = self.collage['article_summary'][4]
          context['five_link'] = self.collage['article_link'][4]
          context['five_keyword'] = self.collage['keyword'][4]
          context['five_left'] = self.collage['img_x'][4]
          context['five_top'] = self.collage['img_y'][4]
          context['five_image'] = self.collage['img'][4]
          context['five_newsimage'] = self.collage['img_article'][4]
        

        if len(self.collage) >=6:
          context['six_title'] = self.collage['article_title'][5]
          context['six_content'] = self.collage['article_summary'][5]
          context['six_link'] = self.collage['article_link'][5]
          context['six_keyword'] = self.collage['keyword'][5]
          context['six_left'] = self.collage['img_x'][5]
          context['six_top'] = self.collage['img_y'][5]
          context['six_image'] = self.collage['img'][5]
          context['six_newsimage'] = self.collage['img_article'][5]

        if len(self.collage) >=7:
          context['seven_title'] = self.collage['article_title'][6]
          context['seven_content'] = self.collage['article_summary'][6]
          context['seven_link'] = self.collage['article_link'][6]
          context['seven_keyword'] = self.collage['keyword'][6]
          context['seven_left'] = self.collage['img_x'][6]
          context['seven_top'] = self.collage['img_y'][6]
          context['seven_image'] = self.collage['img'][6]
          context['seven_newsimage'] = self.collage['img_article'][6]

        if len(self.collage) >=8:
          context['eight_title'] = self.collage['article_title'][7]
          context['eight_content'] = self.collage['article_summary'][7]
          context['eight_link'] = self.collage['article_link'][7]
          context['eight_keyword'] = self.collage['keyword'][7]
          context['eight_left'] = self.collage['img_x'][7]
          context['eight_top'] = self.collage['img_y'][7]
          context['eight_image'] = self.collage['img'][7]
          context['eight_newsimage'] = self.collage['img_article'][7]


        if len(self.collage) >=9:
          context['nine_title'] = self.collage['article_title'][8]
          context['nine_content'] = self.collage['article_summary'][8]
          context['nine_link'] = self.collage['article_link'][8]
          context['nine_keyword'] = self.collage['keyword'][8]
          context['nine_left'] = self.collage['img_x'][8]
          context['nine_top'] = self.collage['img_y'][8]
          context['nine_image'] = self.collage['img'][8]
          context['nine_newsimage'] = self.collage['img_article'][8]



        if len(self.collage) >=10:
          context['ten_title'] = self.collage['article_title'][9]
          context['ten_content'] = self.collage['article_summary'][9]
          context['ten_link'] = self.collage['article_link'][9]
          context['ten_keyword'] = self.collage['keyword'][9]
          context['ten_left'] = self.collage['img_x'][9]
          context['ten_top'] = self.collage['img_y'][9]
          context['ten_image'] = self.collage['img'][9]
          context['ten_newsimage'] = self.collage['img_article'][9]










        

        

        

        

        

        

        

        

        

        
        
        return context