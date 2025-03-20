// NOTES: Resize lets you scale something to actual dimensions

// RESOLUTION SETTINGS
$fa = 1;
$fs = 0.4;

wheel_radius = 6;
base_height = 20;
base_top = 12;
wheel_track = 15;
wheel_size = 20;
wheel_rotation = 40;

// CAR BODY
scale([1.2, 1, 1.2])
{
	rotate([wheel_rotation/3, 0, 0])
	{
		// BASE
		resize([60, 20, base_height])
			sphere(r = 50);
		//cube([60, 20, base_height], center = true);
		// TOP
		translate([5, 0, (base_height/2) 	- 0.01])
			resize([30, 20, base_top])
				sphere(r = 30);
			//cube([30, 20, base_top], center = true);
	}

// WHEELS
// FRONT LEFT
translate([-20, -wheel_track, 0])
	rotate([0, 0, wheel_rotation])
		resize([wheel_size, wheel_size * 0.5, wheel_size])
			sphere(r = wheel_size);
		//cylinder(h = wheel_width, r = wheel_radius, center = true);
// FRONT RIGHT
translate([-20, wheel_track, 0])
	rotate([0, 0, wheel_rotation])
		resize([wheel_size, wheel_size * 0.5, wheel_size])
			sphere(r = wheel_size);
		//cylinder(h = wheel_width, r = wheel_radius, center = true);

// REAR RIGHT
translate([20, wheel_track, 0])
	resize([wheel_size, wheel_size * 0.5, wheel_size])
		sphere(r = wheel_size);
		//cylinder(h = wheel_width, r = wheel_radius, center = true);
// REAR LEFT
translate([20, -wheel_track, 0])
	resize([wheel_size, wheel_size * 0.5, wheel_size])
		sphere(r = wheel_size);
		//cylinder(h = wheel_width, r = wheel_radius, center = true);

// AXLES
// FRONT
translate([-20, 0, 0])
	rotate([90, 0, 0])
		cylinder(h = wheel_track * 2, r = 2, center = true);
// REAR
translate([20, 0, 0])
	rotate([90, 0, 0])
		cylinder(h = wheel_track * 2, r = 2, center = true);
}