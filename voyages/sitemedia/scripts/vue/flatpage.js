var flatpage = new Vue({
  el: "#flatpage",
  delimiters: ['{{', '}}'],
  data: {
    title: {},
    response: {},
    articles: [],
    content: "",
    pathname: "understanding",
    previous: {
      title: "",
      index: 0,
    },
    next: {
      title: "",
      index: 0,
    },
    currentIndex: 0,
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
      axios.get(current.url)
      .then(function (response) {
        vm.content = response.data;
        vm.updateNav();
      })
      .catch(function (error) {
        console.log(error);
      });
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
    var url = host + prefix + this.pathname;
    console.log(url);
    axios.get(url)
    .then(function (response) {
      vm.response = response.data;
      console.log(response);
      // Vue.set(vm.response, response.data);
      var articles = [];
      for (var i = 0; i < response.data.items.length; i++) {
        var article = {
          "url": response.data.items[i].url,
          "class": "indentation-" + response.data.items[i].level,
          "title": response.data.items[i].title,
          "id": i,
          "isActive": false,
        };
        articles.push(article);
      }
      vm.articles = articles;
      vm.navigate("0"); // load initial page
      vm.updateNav();
    })
    .catch(function (error) {
      console.log(error);
    });
  }
})
