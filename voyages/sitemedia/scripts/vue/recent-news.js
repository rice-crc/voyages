var recentNews = new Vue({
  el: "#recent-news",
  delimiters: ['[[', ']]'],
  data: {
    news: []
  },
  watch: {
    title: {
      handler: function() {
      },
      deep: true,
    },
    response: {
      handler: function() {
      },
      deep: true,
    },
  },

  created: function() {
    var vm = this;
    var host = window.location.origin;
    var prefix = "/common/flatpagehierarchy/";
    var pathname = "about/news";
    var url = host + prefix + pathname;
    var articles = [];
    axios.get(url)
    .then(function (response) {
      vm.response = response.data;
      var new_article_urls=[];
      //maximum number of articles to show on the front page
      var max_new_articles=3;
      for (var i = 1; i <= Math.min(vm.response.items.length,max_new_articles); i++) {
      	new_article_urls.push(vm.response.items[vm.response.items.length-i].url)
      };
      //console.log(new_article_urls);
      for (const articleURL of new_article_urls) {
          var title, timestamp;
          //comment out the below line in dev
          //but it's needed in prod
           articleURLhttps = articleURL.replace(/^http:\/\//i, '//');
           axios.get(articleURLhttps).then(function (articleResponse) {
            var htmlStr = articleResponse.data;
            var el = $("<div></div>");
            el.html(htmlStr);
            title = $(".page-title-1", el)[0].innerText;
            timestamp = $(".method-date", el)[0].innerText;
            text = $("p", el)[0].innerText.substring(0, 200) + "...";
            url = articleResponse.request.responseURL.replace(
              "common/getflatpage/about/",
              "about/about#"
            );
            var article = {
              url: url,
              title: title,
              id: new_article_urls.indexOf(articleResponse.request.responseURL),
              timestamp: timestamp,
              text: text,
            };
            //if we're doing this asynchronously, we've got to sort the array that we're building iteratively.
            articles.push(article);
            articles.sort(function(a,b) {
            	return a.id-b.id
            });
            //console.log(articleResponse.request.responseURL);
            //console.log(articles);
            Vue.set(vm, "news", articles);
          })
      }
    })
    .catch(function (error) {
      console.log(error);
    });


  }
})
