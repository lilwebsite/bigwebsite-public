from bigwebsite.include.os import (subprocess, re)

#<iframe style="border: 0; width: 350px; height: 470px;" src="https://bandcamp.com/EmbeddedPlayer/album=1172227681/size=large/bgcol=ffffff/linkcol=0687f5/tracklist=false/transparent=true/" seamless></iframe>
#
embed_width = 350
embed_height = (470, 442) #(album height, track height)
embed = '<iframe style="border: 0; width: {width}px; height: {height}px;" src="https://bandcamp.com/EmbeddedPlayer/{embed_type}={embed_id}/size=large/bgcol=ffffff/linkcol=0687f5/tracklist=false/transparent=true/" seamless></iframe>' #format arguments: (width, height, type, id)

def get_bigwebsite_bandcamp():
	pipe = subprocess.Popen(['curl', '-sG', 'https://bigwebsite.bandcamp.com/'], stdout=subprocess.PIPE)
	found = subprocess.check_output(['grep', 'data-item-id'], stdin=pipe.stdout).decode('UTF-8').split('\n')
	output = []
	for entry in found:
		output.append(re.search(r'(?:data-item-id="(\w+)-(\d+)")', entry, re.IGNORECASE))
		place = len(output)-1
		if output[place] is not None:
			output[place] = {output[place].group(1): output[place].group(2)}
	while True:
		try:
			output.remove(None)
		except ValueError:
			break;
	return output

def formulate_embeds():
	embeds = []
	for entry in get_bigwebsite_bandcamp():
		for key,val in entry.items():
			if key == 'album':
				embeds.append(embed.format(
					width = embed_width,
					height = embed_height[0],
					embed_type = key,
					embed_id = val
				))
				continue;
			embeds.append(embed.format(
				width = embed_width,
				height = embed_height[1],
				embed_type = key,
				embed_id = val
			))
	return embeds
