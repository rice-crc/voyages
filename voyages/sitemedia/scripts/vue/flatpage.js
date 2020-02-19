// please declare data object before initializing this Vue instance
// here is a template
// data = {
//   title: {},
//   response: {},
//   articles: [],
//   content: "",
//   pathname: "your_category_in_flatpage",
//   previous: {
//     title: "",
//     index: 0,
//   },
//   next: {
//     title: "",
//     index: 0,
//   },
//   currentIndex: 0,
// }

var flatpage = new Vue({
  el: "#flatpage",
  delimiters: ['{{', '}}'],
  data: data, // please declare data object before initializing this Vue instance
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

  computed: {
    hasPrev() {
      return (this.currentIndex >= 1);
    },
    hasNext() {
      return (this.currentIndex <= this.articles.length - 2);
    }
  },

  methods: {

    navigate(value) {
      this.articles.forEach(function(article){
        article.isActive = false;
      });
      var current = this.articles[value];
      this.currentIndex = parseInt(value);
      current.isActive = true;
      var vm = this;
      var currentProtocol = location.protocol;
      if (currentProtocol == "https:") {
        current.url = current.url.replace(/^http:\/\//i, 'https://');
      }

      // update breadcrumb
      this.breadcrumb = [];
      for (i = this.currentIndex + 1; i--; i>=0) {
        var currentItem = this.articles[i];
        if (this.breadcrumb.length == 0) {
          this.breadcrumb.unshift(currentItem);
        } else {
          if (this.breadcrumb[0].level > currentItem.level) {
            this.breadcrumb.unshift(currentItem);
          }
        }
        if (currentItem.level <= 0) break;
      }

      var currentURL = current.url;

      axios.get(current.url)
      .then(function (response) {
        // vm.content = response.data;
        $("#center-content-inner").html(response.data)
        // vm.updateNav();
        // use a hash system to determine a particular page
        var hashURL = vm.extractURL(currentURL, vm.pathname, true);
        if (window.location.href.match(/[^#]*/i)) {
          window.location.href = window.location.href.match(/[^#]*/i)[0] + hashURL;
        } else {
          window.location.href = window.location.href + hashURL;
        }
      })
      .catch(function (error) {
        console.log(error);
      });
    },

    getArticleIndex(url) {
      var index = 0;
      this.articles.forEach(function(article, currentArticleIdx) {
        if (article.url.includes(url.slice(0, -3))) { // trim off language tag
          index = currentArticleIdx;
        }
      });
      return index;
    },

    updateNav() {
      var currentLvl = this.response.items[this.currentIndex].level;

      if (this.hasPrev) {
        var previousLvl = this.response.items[this.currentIndex - 1].level;
        var prevStep = currentLvl == previousLvl ? 1:2;
        var prevIndex = this.currentIndex - prevStep;
        Vue.set(this.previous, "index", this.currentIndex - prevStep);
        Vue.set(this.previous, "title", this.response.items[prevIndex].title);
      }

      if (this.hasNext) {
        var nextLvl = this.response.items[this.currentIndex + 1].level;
        var nextStep = currentLvl == nextLvl ? 1:2;
        var nextIndex = this.currentIndex + nextStep;
        Vue.set(this.next, "index", this.currentIndex + nextStep);
        Vue.set(this.next, "title", this.response.items[nextIndex].title);
      }

      // this.next.index = this.currentIndex + nextStep;
      // this.previous.title = this.response.items[prevIndex].title;
      // this.next.title = this.response.items[nextIndex].title;
    },

    navPrevious() {
      this.navigate(this.previous.index);
    },

    navNext() {
      this.navigate(this.next.index);
    },

    extractURL(flatpageURL, delimiter, hasHash) {
      var URLs = flatpageURL.split(delimiter);
      var URL = URLs[1];
      URL = URL.replace(/^\//g, '');
      if (hasHash) URL = "#" + URL;
      return URL;
    }
  },

  mounted: function() {
  },

  // event loop - update the menuAim everytime after it's re-rendered
  updated: function() {

  },

  created: function() {
    var vm = this;
    var host = window.location.origin;
    var prefix = "/common/flatpagehierarchy/";
    var pathname = window.location.pathname;
    var url = host + prefix + this.pathname;

    axios.get(url)
    .then(function (response) {
      vm.response = response.data;
      // console.log(response);
      // Vue.set(vm.response, response.data);
      var articles = [];
      for (var i = 0; i < response.data.items.length; i++) {
        var article = {
          "url": response.data.items[i].url,
          "class": "indentation-" + response.data.items[i].level,
          "title": response.data.items[i].title,
          "id": i,
          "isActive": false,
          "level": response.data.items[i].level
        };
        articles.push(article);
      }
      vm.articles = articles;

      var hashURL = window.location.href.match(/\#(.*)/); // get the URL with the #
      if (hashURL != null && hashURL.length > 0) { // if the URL with the # is matched
        var articleIndex = vm.getArticleIndex(hashURL[1]); 
        vm.navigate(articleIndex); // load a page from URL
      } else {
        vm.navigate("0"); // load initial page
      }
      // vm.updateNav();
    })
    .catch(function (error) {
      console.log(error);
    });
  }
})
