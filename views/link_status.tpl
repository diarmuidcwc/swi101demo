%#template to generate a HTML list
<p>Link Status</p>
<ul>
%for (port,status) in items.iteritems():
  <li>Port {{port}} is {{status}}</li>
%end
</ul>