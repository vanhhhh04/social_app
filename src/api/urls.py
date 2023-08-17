class Endpoint :
    # get all article and ADD article 
    ARTICLE ="/api/articles"
    
    # get one article and delete article
    ARTICLE1 = "/api/articles/<int:id_article>"
    
    # add favorites and unfavorites article 
    ARTICLE2 ="/api/articles/<int:id_article>/favorite"

    #add favorites and unfavorites comments
    ARTICLE3 = "/api/articles/comment/<int:id_comment>/favorite"

    # add favorites and unfavorites comments 
    ARTICLE4 = "/api/articles/nested_comment/<int:id_nested_comment>/favorite"
    
    # add comment to article 
    ARTICLE5 = "/api/articles/<int:id_article>/comments"

    # add nested_comment to comment and get all nested comment from single big comment
    ARTICLE6 = "/api/articles/<int:id_article>/<int:id_comment>/nested_comment"

    # delete comment 
    ARTICLE7 = "/api/articles/<int:id_article>/comments/<int:id_comment>"

    # delete nested comment 
    ARTICLE8 = "/api/articles/<int:id_article>/comments/nested_comment/<int:id_nested_comment>"


    # get current user and register user and update user 
    USER = "/api/user"
    
    # login user
    USER1 = "/api/user/login"

    # notification 
    USER2 = "/api/notification"

    # add message 
    USER3 = "/api/message/<int:id_user>"
    
    # get profile user 
    PROFILE = "/api/profiles"

    # get friend profile with condition
    PROFILE1 = "/api/another_profiles"

    # get comments of one article
    COMMENTS = "/api/articles/<int:id_article>/comments"
   