uniform sampler2D texture;
float blur_radius=0.005;

void main()
{
	vec2 offx = vec2(blur_radius, 0.0);
	vec2 offy = vec2(0.0, blur_radius);

	vec4 pixel = texture2D(texture, gl_TexCoord[0].xy)               * 4.0 +
                 texture2D(texture, gl_TexCoord[0].xy - offx)        * 2.0 +
                 texture2D(texture, gl_TexCoord[0].xy + offx)        * 2.0 +
                 texture2D(texture, gl_TexCoord[0].xy - offy)        * 2.0 +
                 texture2D(texture, gl_TexCoord[0].xy + offy)        * 2.0 +
                 texture2D(texture, gl_TexCoord[0].xy - offx - offy) * 1.0 +
                 texture2D(texture, gl_TexCoord[0].xy - offx + offy) * 1.0 +
                 texture2D(texture, gl_TexCoord[0].xy + offx - offy) * 1.0 +
                 texture2D(texture, gl_TexCoord[0].xy + offx + offy) * 1.0;
	
	vec4 p2 = gl_Color * (pixel / 16.0);

	if( p2.a > 0.2 )
		gl_FragColor =  vec4(0, 0, 0.5, 0.3);//;
	else
		gl_FragColor =  vec4(0, 255, 0, 0);//;
}
