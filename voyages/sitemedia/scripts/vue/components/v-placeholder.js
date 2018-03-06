Vue.component('v-placeholder', {
  props: ['title', 'description'],
  template: `
    <div class="v-form-group">
      <div class="v-title">
        <span>{{title}}</span>
        <span>
          <b-badge
            v-b-tooltip.hover title="Need backend API to support this variable"
            variant="dark">
            Need API
          </b-badge>
        </span>
      </div>
      <div class="v-description">[{{description}}]</div>
    </div>
  `,

  data: function() {
    return {}
  },

})
// end of input
