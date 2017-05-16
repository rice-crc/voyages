export function initialize(application) {
  // application.inject('route', 'foo', 'service:foo');
  // injection allows service to be available across defined scopes
  application.inject('route', 'voyagesSearch', 'service:voyages-search');
  application.inject('controller', 'voyagesSearch', 'service:voyages-search');
}

export default {
  name: 'voyages-search',
  initialize
};
