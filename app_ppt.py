import streamlit as st
from pptx import Presentation
from pptx.util import Inches, Pt
import os
import psutil
#from app_ppt import (ppt_insert_first_title, ppt_insert_summarization, ppt_insert_images)

# Ref for slide types: 
# 0 ->  title and subtitle
# 1 ->  title and content
# 2 ->  section header
# 3 ->  two content
# 4 ->  Comparison
# 5 ->  Title only 
# 6 ->  Blank
# 7 ->  Content with caption
# 8 ->  Pic with caption

def ppt_insert_first_title(ppt_file, insert_title, insert_author, Layout=0, Placeholder=1, start_ppt=False):
    if os.path.exists(ppt_file):
        os.remove(ppt_file)
    prs=Presentation()

    title_slide_layout = prs.slide_layouts[Layout] #建立簡報檔第一張頁面物件
    #使用簡報物件中的方法將上一行建立的第一張頁面物件放進簡報
    slide = prs.slides.add_slide(title_slide_layout)
    #設定第一張頁面的標題 
    title = slide.shapes.title
    title.text = insert_title
    #設定第一張頁面的副標題
    subtitle = slide.placeholders[Placeholder] #設定副標題物件，副標題通常為第2個佔位圖
    subtitle.text = insert_author       

    #將簡報物件存檔
    prs.save(ppt_file)
    if start_ppt:
        os.startfile(ppt_file)

def ppt_insert_summarization(ppt_file, insert_title, summarized_text, Layout=6, Placeholder=1, start_ppt=False):
    if os.path.exists(ppt_file):
        prs=Presentation(ppt_file)
    else:
        prs=Presentation()

    title_slide_layout = prs.slide_layouts[Layout] #建立簡報檔第一張頁面物件
    #使用簡報物件中的方法將上一行建立的第一張頁面物件放進簡報
    #slide = prs.slides.add_slide(title_slide_layout)
    #shapes = slide.shapes

    # To create blank slide layout We have to use 6 as an argument of slide_layouts  
    blank_slide_layout = prs.slide_layouts[6] 
    slide = prs.slides.add_slide(blank_slide_layout)
    left = height = Inches(1) 
    top = Inches(0.8)
    width = Inches(8)
    txBox = slide.shapes.add_textbox(left, top, width, height)
    
    # creating textFrames
    tf = txBox.text_frame
    tf.text = "This is text inside a textbox"
    # adding Paragraphs
    p = tf.add_paragraph()
    p.text = "This is a second paragraph that's bold and italic" 
    p.font.bold = True
    p.font.italic = True
    
    p = tf.add_paragraph()
    p.text = "This is a third paragraph that's big " 
    p.font.size = Pt(40)

    #設定第一張頁面的標題 
    #title = slide.shapes.title
    #title.text = insert_title

    #slide = prs.slides.add_slide(blank_slide_layout)
    left = Inches(1)
    top = Inches(2)
    height = Inches(5) 
    width = Inches(8)
    txBox = slide.shapes.add_textbox(left, top, width, height)
    # creating textFrames
    tf = txBox.text_frame
    tf.text = "自動摘要"

    for sentence, score in summarized_text:
        p = tf.add_paragraph()
        # font 
        p.font.bold = True
        p.font.italic = True
        p.font.size = Pt(24)
        p.text = "{0}: {1}分".format(sentence, score) #再副標題物件輸入文字    

    #將簡報物件存檔
    prs.save(ppt_file)
    if start_ppt:
        os.startfile(ppt_file)

def ppt_insert_summarization2(ppt_file, insert_title, summarized_text, Layout=1, Placeholder=1, start_ppt=False):
    if os.path.exists(ppt_file):
        prs=Presentation(ppt_file)
    else:
        prs=Presentation()

    title_slide_layout = prs.slide_layouts[Layout] #建立簡報檔第一張頁面物件
    #使用簡報物件中的方法將上一行建立的第一張頁面物件放進簡報
    slide = prs.slides.add_slide(title_slide_layout)
    #shapes = slide.shapes
    
    #設定第一張頁面的標題 
    title = slide.shapes.title
    title.text = insert_title

    for sentence, score in summarized_text:
        subtitle = slide.placeholders[Placeholder] #設定副標題物件，副標題通常為第2個佔位圖
        subtitle.append = "{0}: {1}分".format(sentence, score) #再副標題物件輸入文字        

    #將簡報物件存檔
    prs.save(ppt_file)
    if start_ppt:
        os.startfile(ppt_file)

def ppt_insert_images(ppt_file, image_profiles, Layout=1, Placeholder=1, start_ppt=False):
    if os.path.exists(ppt_file):
        prs=Presentation(ppt_file)
    else:
        prs=Presentation()

    
    for img_title, img_file in image_profiles:
        slide = prs.slides.add_slide(prs.slide_layouts[Layout])
        shapes = slide.shapes
        #投影片標題
        title_shape = shapes.title
        title_shape.text = img_title # image_profiles[0][0]    

        # show the figure
        height = Inches(4.5)
        left = top = Inches(3)
        pic = slide.shapes.add_picture(img_file, left, top, height=height)

    #將簡報物件存檔
    prs.save(ppt_file)
    if start_ppt:
        os.startfile(ppt_file)

def app():
    st.title('Automated PPT Generation')

    for proc in psutil.process_iter():
        if proc.name() == 'POWERPNT.EXE':
            proc.kill()

    # page 1
    with open('report/page1/title.txt', mode='r', encoding='utf-8') as f:
        insert_title = f.read()
    with open('report/page1/author.txt', mode='r', encoding='utf-8') as f:
        insert_author = f.read()

    #st.info(insert_title + '\n' +  insert_author)
    ppt_insert_first_title(ppt_file='Summary.pptx', insert_title=insert_title, insert_author=insert_author, start_ppt=False)

    # page 2
    with open('report/page2/title.txt', mode='r', encoding='utf-8') as f:
        insert_title = f.read()
    with open('report/page2/summary.txt', mode='r', encoding='utf-8') as f:
        lines = f.readlines()

    summarized_text = [ (S[0],S[1]) for S in [ L.split(',') for L in lines ] ]

    #st.dataframe(summarized_text)
    ppt_insert_summarization(ppt_file='summary.pptx', insert_title=insert_title, summarized_text= summarized_text, start_ppt=True)
    #summarized_text = [('AAA',0.5),('BBB',0.34),('CCC',0.9)]

    image_profiles=[(F.split('.')[0],os.path.join('report/page3/img/',F)) for F in os.listdir('report/page3/img')]
    st.dataframe(image_profiles)
    #[('Sentiment Analysis - Company','report\page3\img/sentiment1.jpg'), ('Sentiment Analysis - Source', 'report\page3\img/sentiment2.jpg'), ('Sentiment Analysis - Source', 'report\page3\img/sentiment3.jpg'), ('ESG Media Trend - Environment', 
    # 'report\page3\img/esgenvironment.jpg')]
    ppt_insert_images(ppt_file='Summary.pptx', image_profiles=image_profiles, start_ppt=True)


