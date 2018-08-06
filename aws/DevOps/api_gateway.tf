resource "aws_api_gateway_rest_api" "odl" {
   name = "OpenDataLab API"
   description = "Open Data Lab API for creating and terminating instances for students"
}


// STAND UP RESOURCES

// Declare the stand up path
resource "aws_api_gateway_resource" "stand_up" {
   rest_api_id = "${aws_api_gateway_rest_api.odl.id}"
   parent_id = "${aws_api_gateway_rest_api.odl.root_resource_id}"
   path_part = "standup"
}

// Add method to stand_up path
resource "aws_api_gateway_method" "stand_up" {
   rest_api_id = "${aws_api_gateway_rest_api.odl.id}"
   resource_id = "${aws_api_gateway_resource.stand_up.id}"
   http_method = "POST"
   authorization = "NONE"

}

// Integrate the lamda function for stand up
resource "aws_api_gateway_integration" "stand_up_integration" {
   rest_api_id = "${aws_api_gateway_rest_api.odl.id}"
   resource_id = "${aws_api_gateway_resource.stand_up.resource_id}"

   http_method = "POST"
   type = "AWS_PROXY"
   uri = "${aws_lambda_function.stand_up.invoke_arn}"
   
}


// STAND DOWN RESOURCES

// Declare the stand down path
resource "aws_api_gateway_resource" "stand_down" {
   rest_api_id = "${aws_api_gateway_rest_api.odl.id}"
   parent_id = "${aws_api_gateway_rest_api.odl.root_resource_id}"
   path_part = "standdown"
}

// Add method to stand_up path
resource "aws_api_gateway_method" "stand_down" {
   rest_api_id = "${aws_api_gateway_rest_api.odl.id}"
   resource_id = "${aws_api_gateway_resource.stand_down.id}"
   http_method = "POST"
   authorization = "NONE"

}

// Integrate the lamda function for stand down
resource "aws_api_gateway_integration" "stand_down_integration" {
   rest_api_id = "${aws_api_gateway_rest_api.odl.id}"
   resource_id = "${aws_api_gateway_resource.stand_down.resource_id}"

   http_method = "POST"
   type = "AWS_PROXY"
   uri = "${aws_lambda_function.stand_down.invoke_arn}"
   
}




// Create a Deployment to activate and expose API
resource "aws_api_gateway_deployment" "test_deployment" {
   depends_on = [
      "aws_api_gateway_integration.stand_up",
      "aws_api_gateway_integration.stand_down"
   ]
   
   rest_api_id = "${aws_api_gateway_rest_api.odl.id}"
   stage_name = "test"
}
