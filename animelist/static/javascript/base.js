function show_filters() {
  let image = document.querySelector('.show-filters');
  if (image.src === 'http://127.0.0.1:8000/static/icons/filter.png') {
    image.src = 'http://127.0.0.1:8000/static/icons/filter (1).png';
    document.querySelector('.filter-options').classList.add('filter-options-show');
  } else {
    document.querySelector('.filter-options').classList.remove('filter-options-show');
    image.src = 'http://127.0.0.1:8000/static/icons/filter.png';
  }
}

