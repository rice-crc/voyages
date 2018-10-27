// v-panel
Vue.component('v-flatpage', {
  props: ["title", "list"],
  template: `
    <div>
      <div class="sidebar-header-container">
        <div class="sidebar-title-1">{{title}}</div>
      </div>
      <div v-for="item in list" v-bind:class="[item.class, item.isActive ? 'article-list-active':''  ]">
        <a class="article-list-item" :id="item.id"
            @click=click>{{item.title}}</a>
      </div>
    </div>
  `,

  data: function(){
    return {};
  },

  methods: {
    click (event) {
      this.$emit('clicked', event.target.id);
    }
    // apply() {
    //   this.$emit('apply', this.group, this.subGroup, this.filtersValue);
    // },
    // reset(group, subGroup) {
    //   this.$emit('reset', this.group, this.subGroup);
    // }
  },

  watch: {
    // response: {
    //   handler: function() {
    //     var vm = this;
    //     this.response.forEach(function(response){
    //       vm.articles.push(response);
    //     });
    //   },
    //   deep: true,
    // },
    // filters: {
    //   handler: function(){
    //     this.applyDisabled = (this.filters.count.changed > 0) ? false:true;
    //     this.resetDisabled = (this.filters.count.changed > 0 || this.filters.count.activated > 0) ? false:true;
    //     this.filtersValue = this.filters;
    //   },
    //   deep: true,
    // },

  },
  created: function() { // load value initially
    // this.titleValue = this.title;
    // this.idValue = hyphenate(this.title);
    // this.filtersValue = this.filters;
  }

})
// v-flatpage
