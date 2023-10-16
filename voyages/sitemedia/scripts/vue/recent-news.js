var recentNews = new Vue({
//   el: "#recent-news",
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
    var prefix = '/common/flatpagehierarchy/';
    var pathname = 'about/news';
    var url = host + prefix + pathname;

    var articleMaxNum = 10;
    var articles = [];

    axios.get(url)
    .then(function (response) {
      vm.response = response.data;

      articles = [...response.data.items].reverse().slice(0, articleMaxNum);
//       console.log('ARTICLES',articles)
      var article = [];
      articles.forEach((article, i) => {
        article.url = article.url.replace(/^http:\/\//i, '//');

        axios.get(article.url)
        .then(function (articleResponse) {
//          console.log("ARTICLE RESPONSE",articleResponse.data)
          var el = $("<div></div>");
          el.html(articleResponse.data);
//           console.log("EL",el)
//           console.log($(".page-title-1", el).innerText)
//           console.log(el)
          article.id = i;
//           article.title = $(".page-title-1", el).innerText;
//           article.timestamp = $(".method-date", el).innerText;
//           article.text = $("p", el)[0].innerText.substring(0, 200) + "...";
          article.url = article.url.replace(
            "common/getflatpage/about/",
            "about/about#"
          );
        });
      });

      Vue.set(vm, "news", articles);
    });
  }

})
