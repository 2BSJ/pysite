# Pycharm 에서 Django 프로젝트 시작하기

- 기본적으로 장고 프로젝트 한 개당 한 개의 DB를 사용한당.
- 장고 프로젝트에는 기본적으로 관리프로그램이 내장되어 있기때문에

- postgresql 에 db 생성 및 계정생성 접근 권한 부여
    -create database pysite
    -create user pysite with password 'pysite';
    -grant all privileges on all tables in schema public to pysite;
    -data/pg_hba.conf 접근 설정

1. pysite 프로젝트 생성(python 프로젝트)

2. Django 설치
[터미널]
pip install django

3. 장고 프로젝트 생성
[터미널]
django-admin startproject python_ch3  
문제점 - python_ch3 하위에 python_ch3 쟝고 프로젝트가 만들어짐

4. 디렉토리 정리  
   ->pycharm 프로젝트와 django 프로젝트의 디렉토리를 일치시키느은 작어업
    
5. psycopg2(postgres db lib) 설치
[터미널] pip install psycopg2
    
7. settins.py 설정
    1) TIME_ZONE = 'Asia/Seoul'
    2) DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'pysite',
        'USER': 'pysite',
        'PASSWORD' : 'pysite',
        'HOST' : '192.168.1.92',
        'PORT' : 5432
    }
}

    3) Template 디렉토리 설정
    TEMPLATE=[
        ...
        'DIRS': [os.path.join(BASE_DIR,'template')],
        ...
    ]
    
    pysite
        |
        |-------- templates(생성)

8. 장고 프로젝트의 기본 관리 어플리케이션이 사용하는 테이블
[터미널] python manage.py migrate

9. 장고 프로젝트의 기본 관리 어플리케이션 로그인 계정 생성하기(관리계정 생성)
[터미널] python manage.py createsuperuser 

10. 지금까지 작업 내용 확인하기
[터미널] python manage.py runserver 0.0.0.0:8888

11. 관리페이지 들어가기
localhost:8888/admin

-------------------------

# Application 작업
1. helloworld
    1. 어플리케이션 추가
    [터미널] python manage.py startapp main
    2. 어플리케이션 등록(settings.py)
       INSTALLED_APPS =[
          'main',
           ....
           ....
       ]
    3. template
          |---- main
       어플리케이션 template 디렉토리 생성
    4. Model 정의(생략)
    5. urls.py에서 url-view의 handler 매핑
    6. views.py에서 핸들러 함수 구현(요청처리, 모델작업, 응답처리)
    7. 화면이 필요한 경우, 해당 template 작업
2.user
    1.어플리케이션 추가
    [터미널] python manage.py startapp emaillist
    2. 어플리케이션 등록(settings.py)
        INSTALLED_APPS =[
            'user',
            ....
            ....
        ]
        3.tempalate
               |--- user
                어플리케이션 template 디렉토리 생성        
    4-1. Model 정의
    4-2. admin.py 에
        admin site.register(User)
    4-3 migration 이름의 DDL python 모듈을 생성
        python manage.py makemigrations
    4.4. 물리DB와 스키마 동기화 작업을 한다.
        python manage.py migrate
    5. urls.py에서 url-view의 handler 매핑
    6. views.py에서 핸들러 함수 구현(요청처리,모델작업)
    7. 화면이 필요한 경우, 해당 template 작업