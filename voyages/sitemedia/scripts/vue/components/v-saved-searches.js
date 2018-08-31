Vue.component('v-saved-searches', {
  props: ['title', 'description', 'saved'],
  template: `
    <div class="v-form-group">
      <div class="v-title">
        <span>{{title}}<span> ({{saved.length}})</span></span>
        <span>
          <b-button variant="info" size="sm" @click="click">
             Save
          </b-button>
        </span><!-- reserved for right aligned content -->
      </div>
      <div class="v-description">
        <div v-if="saved.length">Here are the queries saved during this session.</div>
        <div v-else>No query saved during this session.</div>
      </div>

      <div class="flex-between v-saved-searches-header" v-if="saved.length">
        <div class="v-title">URL</div>
      </div>

      <div class="flex-between v-saved-searches-item" v-for="search in saved">
        <div :id="search.saved_query_id">
          {{search.saved_query_url}}
        </div>
        <div>
          <b-button variant="info" size="sm" @click="load">
             Load
          </b-button>
          <b-button variant="primary" size="sm" @click="clip(search.saved_query_id)" data-clipboard-action="copy" :data-clipboard-target="search.saved_query_id">
             Copy
          </b-button>
        </div>
      </div>

    </div>
  `,

  methods: {
    clip(value) {
      this.$emit('clip', value);
    },
    load() {
      this.$emit('clip', this);
    },
    click() {
      debugger;
      this.$emit('save');
    },
  },

  created: function(){
    new Clipboard('.btn');
  }

});
