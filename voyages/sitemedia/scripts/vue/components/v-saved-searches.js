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
          <b-button variant="outline-secondary" size="sm" @click="load(search.saved_query_id)">
             Load
          </b-button>
          <b-button variant="info" size="sm"
            v-clipboard:copy="search.saved_query_url"
            v-clipboard:success="onCopy"
            v-clipboard:error="onError">Copy</b-button>
        </div>
      </div>

    </div>
  `,

  methods: {
    load(saved_query_id) {
      this.$emit('load', saved_query_id);
    },
    click() {
      this.$emit('save');
    },
    onCopy: function (e) {
      alert('Your URL ' + e.text + " is copied")
    },
    onError: function (e) {
      alert('Failed to copy URL')
    }
  },

  created: function(){
  }

});
