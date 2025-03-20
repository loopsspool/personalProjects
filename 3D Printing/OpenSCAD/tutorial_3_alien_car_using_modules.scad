// NOTES: Resize lets you scale something to actual dimensions

// RESOLUTION SETTINGS
//$fa = 1;
//$fs = 0.4;

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
	wheel(wheel_radius = 10, side_spheres_radius = 50, hub_thickness = 4, cylinder_radius = 2);
	
// FRONT RIGHT
translate([-20, wheel_track, 0])
	wheel(wheel_radius = 10, side_spheres_radius = 50, hub_thickness = 4, cylinder_radius = 2);

// REAR RIGHT
translate([20, wheel_track, 0])
	wheel(wheel_radius = 12, side_spheres_radius = 20, hub_thickness = 6, cylinder_radius = 4);
	
// REAR LEFT
translate([20, -wheel_track, 0])
	wheel(wheel_radius = 12, side_spheres_radius = 20, hub_thickness = 6, cylinder_radius = 4);

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

module wheel(wheel_radius=10,
    side_spheres_radius=50,
    hub_thickness=4,
    cylinder_radius=2) 
{
    cylinder_height=2*wheel_radius;
    difference() {
        // Wheel sphere
        sphere(r=wheel_radius);
        // Side sphere 1
        translate([0,side_spheres_radius + hub_thickness/2,0])
            sphere(r=side_spheres_radius);
        // Side sphere 2
        translate([0,- (side_spheres_radius + hub_thickness/2),0])
            sphere(r=side_spheres_radius);
        // Cylinder 1
        translate([wheel_radius/2,0,0])
            rotate([90,0,0])
            cylinder(h=cylinder_height,r=cylinder_radius,center=true);
        // Cylinder 2
        translate([0,0,wheel_radius/2])
            rotate([90,0,0])
            cylinder(h=cylinder_height,r=cylinder_radius,center=true);
        // Cylinder 3
        translate([-wheel_radius/2,0,0])
            rotate([90,0,0])
            cylinder(h=cylinder_height,r=cylinder_radius,center=true);
        // Cylinder 4
        translate([0,0,-wheel_radius/2])
            rotate([90,0,0])
            cylinder(h=cylinder_height,r=cylinder_radius,center=true);
    }
}