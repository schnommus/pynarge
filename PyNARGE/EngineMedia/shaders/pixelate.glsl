uniform sampler2D texture;
float pixel_threshold = 0.01;

void main()
{
    float factor = 1.0 / (pixel_threshold + 0.001);
	vec2 pos = floor(gl_TexCoord[0].xy * factor + 0.5) / factor;
	gl_FragColor = texture2D(texture, pos) * gl_Color;	
}
