wheel_track = 15;

module body(base_length = 70, base_height = 8, width = 20)
{
	top_length = 0.75 * base_length;
	top_height = 1.2 * base_height;
	
	// base
	cube([base_length, width, base_height], center = true);
	
	// top
	translate([0, 0, base_height/2 + top_height/2])
		cube([top_length, width, top_height], center = true);
}

module axles()
{
	
};

body();