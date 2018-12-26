from django.urls import path, include
from django.conf.urls import url
from  rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns


from . import views

from rest_framework.schemas import get_schema_view
from rest_framework_swagger.renderers import SwaggerUIRenderer, OpenAPIRenderer


# 路由
# router = routers.DefaultRouter()
# router.register(r'crawler1',views.CrawlerConfigList,base_name='crawler')
# router.register(r'crawler_config_detail',views.CrawlerConfigDetail,base_name='crawler_config_detail')

schema_view = get_schema_view(title='数据挖掘 API', renderer_classes=[OpenAPIRenderer, SwaggerUIRenderer])


crawler_config_list = views.CrawlerConfigViewSet.as_view({
    'get':'list',
    'post':'create'
})

crawler_config_detail = views.CrawlerConfigViewSet.as_view({
    'get':'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

video_list = views.VideoViewSet.as_view({
    'get':'list',
    'post':'create'
})

video_detail = views.VideoViewSet.as_view({
    'get':'retrieve',
    'put': 'update',
    'patch': 'partial-update',
    'delete': 'destroy'
})

router = routers.DefaultRouter()
router.register(r'videos', views.VideoViewSet)
router.register(r'crawlerconfigs', views.CrawlerConfigViewSet)
router.include_format_suffixes = False

urlpatterns = format_suffix_patterns([
    url(r'^docs/', schema_view, name="docs"),
    path('', include(router.urls))
])
