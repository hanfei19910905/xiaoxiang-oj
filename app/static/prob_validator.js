$(document).ready(function() {
    $("#fileupload").bootstrapValidator({
        message: 'This value is not valid',
        feedbackIcons: {
            valid: 'glyphicon glyphicon-ok',
            invalid: 'glyphicon glyphicon-remove',
            validating: 'glyphicon glyphicon-refresh'
        },
        submitButtons: 'button[type="submit"]',
        fields: {
            source: {
                message: 'The source file is not valid',
                validators: {
                    file: {
                        extension: 'py,zip',
                        // type: 'application/zip,text/x-script.phyton',
                        message: 'You can only upload py file or zip file.'
                    },
                    notEmpty: {
                        message: 'You should choose a source file and upload.'
                    }
                }
            },
            result: {
                message: 'The result file is not valid',
                validators: {
                    notEmpty: {
                        message: 'You should choose a result file and upload.'
                    },
                    file: {
                        extension: 'csv,zip',
                        message: 'You can only upload py file or zip file.'
                    }
                }
            }
        }
    });
});