// Simple script to confirm JavaScript is working
console.log('Vercel deployment is working correctly!');

document.addEventListener('DOMContentLoaded', function() {
  // Add a timestamp to show when the page was loaded
  const footer = document.createElement('footer');
  footer.style.textAlign = 'center';
  footer.style.marginTop = '30px';
  footer.style.color = '#666';
  footer.style.fontSize = '0.8rem';
  footer.innerHTML = `<p>Page loaded at: ${new Date().toLocaleString()}</p>`;
  document.body.appendChild(footer);
}); 