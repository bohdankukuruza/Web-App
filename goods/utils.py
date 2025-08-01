from django.db.models.expressions import result

from goods.models import Product
from django.db.models import Q
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, SearchHeadline

def q_search(query):

    if query.isdigit() and len(query) <= 5:
        return Product.objects.filter(id=int(query))

    vector = SearchVector("name", config='russian') + SearchVector("description", config='russian')
    search_query = SearchQuery(query, config='russian')

    result = Product.objects.annotate(rank=SearchRank(vector, search_query)).filter(rank__gt=0).order_by("-rank")

    result = result.annotate(
        headline=SearchHeadline(
            "name",
            query,
            start_sel='<span style="background-color: yellow;">',
            stop_sel='</span>',
        )
    )
    result = result.annotate(
        bodyline=SearchHeadline(
            "description",
            query,
            start_sel='<span style="background-color: yellow;">',
            stop_sel='</span>',
        )
    )

    return result

    # keywords = [word for word in query.split() if len(word) > 2]
    #
    # q_objects = Q()
    #
    # for token in keywords:
    #     q_objects |= Q(description__icontains=token)
    #     q_objects |= Q(name__icontains=token)
    #
    # return Product.objects.filter(q_objects)