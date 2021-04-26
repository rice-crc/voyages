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
    //in dev, you can dodge a cors block with:
    // var host=http://127.0.0.1:8100
    var prefix = "/common/flatpagehierarchy/";
    var pathname = "about/news";
    var url = host + prefix + pathname;
    var articles = [];
    axios.get(url)
    .then(function (response) {
      vm.response = response.data;
      for (var i = 0; i < Math.min(vm.response.items.length,2); i++) {
          articleURL = vm.response.items[i].url;
          var title, timestamp;
          axios.get(articleURL).then(function (articleResponse) {
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
              id: i,
              timestamp: timestamp,
              text: text,
            };

            articles.push(article);
            Vue.set(vm, "news", articles);
          })
      }
    })
    .catch(function (error) {
      console.log(error);
    });


  }
})