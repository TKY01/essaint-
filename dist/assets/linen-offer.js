(() => {
  const handle = 'linen-pants-unisex';
  const tiers = [{ quantity: 1, price: 3600 }, { quantity: 2, price: 3300 }, { quantity: 3, price: 3200 }];
  const unitPrice = quantity => quantity >= 3 ? 3200 : quantity === 2 ? 3300 : 3600;
  function mount(product) {
    const U = window.EssaintUI;
    const form = document.querySelector('#p-form');
    const available = product.variants.find(v => v.available);
    const choices = Array(3).fill(available?.id || product.variants[0].id);
    let quantity = 1;
    form.classList.add('linen-offer');
    form.innerHTML = `<fieldset class="linen-tiers"><legend>Build your linen set</legend>${tiers.map(t => `<label class="linen-tier"><input type="radio" name="linen-tier" value="${t.quantity}" ${t.quantity === 1 ? 'checked' : ''}><span class="linen-tier-copy"><span class="linen-tier-title">${t.quantity} ${t.quantity === 1 ? 'pair' : 'pairs'}${t.quantity === 2 ? '<span class="linen-popular">Most popular</span>' : ''}</span><span class="linen-tier-rate">${U.money(t.price)} each</span></span><span class="linen-tier-total">${U.money(t.quantity * t.price)}${t.quantity > 1 ? `<small>Save ${U.money(t.quantity * (3600 - t.price))}</small>` : ''}</span></label>`).join('')}</fieldset><div class="linen-choices"></div><div class="linen-summary" aria-live="polite"></div><button class="button" type="submit" ${available ? '' : 'disabled'}>Add to bag</button>`;
    const update = () => {
      form.querySelector('.linen-choices').innerHTML = choices.slice(0, quantity).map((id, i) => `<div class="linen-piece"><label for="${i ? 'p-variant-' + (i + 1) : 'p-variant'}">${quantity > 1 ? 'Pair ' + (i + 1) + ' / ' : ''}Size & color</label><select id="${i ? 'p-variant-' + (i + 1) : 'p-variant'}" data-linen-piece="${i}">${product.variants.map(v => `<option value="${v.id}" ${v.id === id ? 'selected' : ''} ${v.available ? '' : 'disabled'}>${U.esc(v.title)}${v.available ? '' : ' — Sold out'}</option>`).join('')}</select></div>`).join('');
      const total = quantity * unitPrice(quantity);
      form.querySelector('.linen-summary').innerHTML = `<span>${quantity} ${quantity === 1 ? 'pair' : 'pairs'} · ${U.money(unitPrice(quantity))} each</span><strong>${U.money(total)}</strong>`;
      document.querySelector('#p-price').textContent = U.money(unitPrice(quantity)) + ' / pair';
    };
    form.addEventListener('change', event => {
      if (event.target.name === 'linen-tier') { quantity = Number(event.target.value); update(); }
      if (event.target.hasAttribute('data-linen-piece')) choices[Number(event.target.dataset.linenPiece)] = Number(event.target.value);
    });
    form.onsubmit = event => {
      event.preventDefault();
      const items = [];
      for (const id of choices.slice(0, quantity)) {
        const existing = items.find(item => item.id === id);
        if (existing) existing.quantity++;
        else items.push({ id, quantity: 1 });
      }
      U.addItems(items, event.submitter);
    };
    update();
  }
  window.EssaintLinenOffer = { handle, tiers, unitPrice, mount };
})();
