Vue.component('v-saved-searches', {
  props: ['title', 'description', 'saved'],
  template: `
    <div class="v-form-group" v-if="saved.length">
      <div class="v-title">
        <span>{{title}}<span v-if="saved.length"> ({{saved.length}})</span></span>
        <span>

        </span><!-- reserved for right aligned content -->
      </div>
      <div class="v-description" v-text="description"></div>

      <div class="row" v-for="search in saved">
        <div class="col-md-3" :id="search.key">
          {{search.key}}
        </div>
        <div class="col-md-5">
          {{search.searchTerms}}
        </div>
        <div class="col-md-4 text-right">
          <b-button variant="info" size="sm" @click="load">
             Load
          </b-button>
          <b-button variant="primary" size="sm" @click="clip" data-clipboard-action="copy" :data-clipboard-target="search.key">
             Share
          </b-button>
        </div>
      </div>

    </div>
  `,
  methods: {
    clip() {
      this.$emit('clip');
    },
    load() {
      this.$emit('clip');
    }
  },
  created: function(){
    debugger;
    new Clipboard('.btn');
  }

});
