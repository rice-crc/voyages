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
    var pathname = "about";
    var url = host + prefix + pathname;
    var articles = [];

    axios.get(url)
    .then(function (response) {
      vm.response = response.data;
      for (var i = 0; i < response.data.items.length; i++) {
        if (response.data.items[i].url.match(/\/about\/news\/[0-9]+\/news\//)) {
          articleURL = response.data.items[i].url;
          var title, timestamp;
          axios.get(articleURL)
          .then(function (artileResponse) {
            var htmlStr = artileResponse.data, html = $.parseHTML(htmlStr);
            
            var el = $("<div></div>");
            el.html(htmlStr);
            title = $(".page-title-1", el)[0].innerText;
            timestamp = $(".method-date", el)[0].innerText;
            text = $("p", el)[0].innerText.substring(0, 200) + "...";
            url = response.data.items[i - 1].url.replace(
              "common/getflatpage/about/",
              "about/about#"
            );
            var article = {
              url: url,
              title: title,
              id: i,
              timestamp: timestamp,
              text: text
            };

            articles.push(article);
            Vue.set(vm, "news", articles);
          });
          
        }
      }
    })
    .catch(function (error) {
      console.log(error);
    });


  }
})