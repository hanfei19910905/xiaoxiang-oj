$(document).ready(function() {
    $("#fileupload").bootstrapValidator({
        message: 'This value is not valid',
        feedbackIcons: {
            valid: 'glyphicon glyphicon-ok',
            invalid: 'glyphicon glyphicon-remove',
            validating: 'glyphicon glyphicon-refresh'
        },
        submitButtons: 'button[id="submit"]',
        fields: {
            name: {
                message: 'The name is not valid',
                validators: {
                    notEmpty: {
                        message: 'You should input data name.'
                    },
                    regexp: {
                        regexp: /^[^\s]+$/i,
                        message: 'You can not input a data name with invalid characters.'
                    }
                }
            },
            train: {
                message: 'The train file is not valid',
                validators: {
                    file: {
                        extension: 'csv',
                        message: 'You can only upload csv file.'
                    },
                    notEmpty: {
                        message: 'You should choose a csv file and upload.'
                    }
                }
            },
            test1: {
                message: 'The test1 file is not valid',
                validators: {
                    file: {
                        extension: 'csv',
                        message: 'You can only upload csv file.'
                    },
                    notEmpty: {
                        message: 'You should choose a csv file and upload.'
                    }
                }
            },
            test2: {
                message: 'The test2 file is not valid',
                validators: {
                    file: {
                        extension: 'csv',
                        message: 'You can only upload csv file.'
                    },
                    notEmpty: {
                        message: 'You should choose a csv file and upload.'
                    }
                }
            },
        }
    });
});