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
  },

})
// v-flatpage
