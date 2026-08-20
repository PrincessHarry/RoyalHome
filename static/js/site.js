// ===== Mobile menu =====
document.addEventListener('DOMContentLoaded', function () {
  const btn = document.getElementById('mobileMenuBtn');
  const menu = document.getElementById('mobileMenu');
  if (btn && menu) {
    btn.addEventListener('click', () => menu.classList.toggle('hidden'));
  }

  // ===== Reveal on scroll =====
  const revealEls = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window) {
    const io = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('reveal-visible');
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0.15 });
    revealEls.forEach((el) => io.observe(el));
  } else {
    revealEls.forEach((el) => el.classList.add('reveal-visible'));
  }

  // ===== AI Concierge widget =====
  const toggle = document.getElementById('conciergeToggle');
  const panel = document.getElementById('conciergePanel');
  const closeBtn = document.getElementById('conciergeClose');
  const form = document.getElementById('conciergeForm');
  const input = document.getElementById('conciergeInput');
  const messages = document.getElementById('conciergeMessages');
  const chips = document.querySelectorAll('.concierge-chip');

  if (toggle && panel) {
    toggle.addEventListener('click', () => {
      panel.classList.toggle('hidden');
      if (!panel.classList.contains('hidden')) input.focus();
    });
    closeBtn.addEventListener('click', () => panel.classList.add('hidden'));
  }

  function addMessage(text, from) {
    const wrap = document.createElement('div');
    if (from === 'user') {
      wrap.className = 'ml-auto bg-ink text-white rounded-2xl rounded-tr-sm px-4 py-3 max-w-[85%] whitespace-pre-line';
    } else {
      wrap.className = 'bg-white border border-grey-200 rounded-2xl rounded-tl-sm px-4 py-3 max-w-[85%] whitespace-pre-line';
    }
    wrap.textContent = text;
    messages.appendChild(wrap);
    messages.scrollTop = messages.scrollHeight;
  }

  function typingIndicator() {
    const wrap = document.createElement('div');
    wrap.className = 'bg-white border border-grey-200 rounded-2xl rounded-tl-sm px-4 py-3 max-w-[60%] text-grey-400';
    wrap.id = 'typingIndicator';
    wrap.textContent = 'Xcep is typing…';
    messages.appendChild(wrap);
    messages.scrollTop = messages.scrollHeight;
  }

  function aiReply(msg) {
    const m = msg.toLowerCase();
    if (m.includes('rate') || m.includes('price') || m.includes('cost')) {
      return "Our rooms start from ₦65,000/night for a Standard Room, up to ₦220,000/night for the Presidential Suite. Prices flex with demand — want me to check live rates for your dates on the Rooms page?";
    }
    if (m.includes('pool')) {
      return "The rooftop and garden pools are open daily 6:00am – 9:00pm. Poolside cabanas can be reserved through Amenities → Pool & Recreation.";
    }
    if (m.includes('recommend') || m.includes('suggest')) {
      return "Happy to help! Tell me: is this for business or leisure, how many guests, and do you want a city/mountain view? I'll match you to a room type instantly.";
    }
    if (m.includes('spa') || m.includes('gym') || m.includes('massage')) {
      return "Our Spa & Wellness centre offers massages, facials and a fully-equipped gym, open 6am–10pm daily. I can add a spa session as a booking add-on if you like.";
    }
    if (m.includes('restaurant') || m.includes('food') || m.includes('eat') || m.includes('jollof') || m.includes('menu')) {
      return "The Signature Restaurant serves breakfast 6–10am, lunch 12–4pm and dinner 6–10pm, plus 24/7 room service. Want me to place a room-service order for you? Just tell me your room number and what you'd like.";
    }
    if (m.includes('towel') || m.includes('laundry') || m.includes('housekeep')) {
      return "Got it — I've logged that request for housekeeping. If you're already checked in, guests can also track order status live from the My Stay portal.";
    }
    if (m.includes('event') || m.includes('conference') || m.includes('wedding')) {
      return "Our Grand Event Hall seats up to 600 guests and our Conference Room fits 80 boardroom-style. Head to Events & Conferences to request a custom quote in minutes.";
    }
    if (m.includes('location') || m.includes('address') || m.includes('where')) {
      return "We're located at Atiku Abubakar Street Junction, Rayfield, Jos, Plateau State — 12 minutes from Jos Terminus and close to Rayfield Park.";
    }
    if (m.includes('wifi') || m.includes('power') || m.includes('light') || m.includes('nepa')) {
      return "Every room has dedicated fibre WiFi, and the hotel runs on 24/7 solar-backed power — so you'll never lose light, even during outages.";
    }
    if (m.includes('bring') || m.includes('order') || /room\s*\d+/.test(m)) {
      return "Order noted! I've forwarded this to the relevant department (Kitchen/Housekeeping) for your room. You'll see live status updates (New → Acknowledged → In Progress → Ready → Delivered) in your My Stay dashboard.";
    }
    if (m.includes('hello') || m.includes('hi') || m.includes('good')) {
      return "Hello! Welcome to Xceptional Place Hotel. I can help with room recommendations, bookings, dining, amenities, or placing an in-stay request. What would you like to do?";
    }
    return "Thanks for that! For detailed help I'd recommend browsing Rooms & Suites or Events, or reach our human team on WhatsApp at +234 803 000 1122. Is there anything else I can check for you?";
  }

  function handleSend(text) {
    if (!text.trim()) return;
    addMessage(text, 'user');
    input.value = '';
    typingIndicator();
    setTimeout(() => {
      const t = document.getElementById('typingIndicator');
      if (t) t.remove();
      addMessage(aiReply(text), 'ai');
    }, 700 + Math.random() * 500);
  }

  if (form) {
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      handleSend(input.value);
    });
  }
  chips.forEach((chip) => {
    chip.addEventListener('click', () => handleSend(chip.textContent));
  });
});
